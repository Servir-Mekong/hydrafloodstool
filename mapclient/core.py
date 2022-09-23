import hydrafloods as hf
from sqlite3 import Date
import time
import os
import json
import ee
from datetime import datetime, timedelta, date
from ee.ee_exception import EEException
from django.http import JsonResponse
from django.conf import settings
import matplotlib.pyplot as plt
from turtle import st
from django.core import serializers
from django.http import HttpResponse
import numpy as np
import base64
import matplotlib as mpl
mpl.use('Agg')
mpl.rcParams.update({'font.size': 14})

# /////////////////////////////////////////////


class MainGEEApi():

    # # Get list of available dates
    # def getDateList(self):
    #     pickup_dict = {}

    #     def imgDate(d):
    #         return ee.Date(d).format("YYYY-MM-dd")
    #     ImageCollection = ee.ImageCollection(
    #         "projects/servir-mekong/hydrafloodsS1Daily")
    #     dates = ee.List(ImageCollection.aggregate_array(
    #         "system:time_start")).map(imgDate).getInfo()
    #     return dates

    # ===================== Precipitation Map ===================== */

    def getTileLayerUrl(self, ee_image_object):
        map_id = ee.Image(ee_image_object).getMapId()
        tile_url_template = str(map_id['tile_fetcher'].url_format)
        return tile_url_template

    def getEELMap(self):
        lmap = ee.Image("users/kamalhosen/kh_all")
        mkmap = lmap.selfMask()
        elMap = self.getTileLayerUrl(mkmap.visualize(
            palette=["yellow", "orange", "red", "blue", "green"], min=1, max=5))
        return elMap

    # Get precipitation map
    def getPrecipMap(self, date, accumulation=1, cmap_name='nipy_spectral'):
        def _accumulate(ic, date, ndays=1):
            eeDate = ee.Date(date)
            ic_filtered = ic.filterDate(
                eeDate.advance(-(ndays-1), 'day'), eeDate.advance(1, 'day'))
            accum_img = ee.Image(ic_filtered.sum())
            return accum_img.mask(accum_img.gt(1))

        if int(accumulation) not in [1, 3, 7]:
            raise NotImplementedError(
                'Selected accumulation value is not yet implemented, options are: 1, 3, 7')

        ic = ee.ImageCollection(
            'JAXA/GPM_L3/GSMaP/v6/operational').select(['hourlyPrecipRateGC'])

        ranges = {1: [1, 100], 3: [1, 250], 7: [1, 500]}
        crange = ranges[int(accumulation)]

        accum = _accumulate(ic, date, int(accumulation))
        nBands = len(accum.bandNames().getInfo())
        test = nBands > 0

        cmap = mpl.cm.get_cmap(cmap_name, 100)

        hexcodes = []
        for i in range(cmap.N):
            # will return rgba, we take only first 3 so we get rgb
            rgb = cmap(i)[:3]
            hexcodes.append(mpl.colors.rgb2hex(rgb))
        colormap = ','.join(hexcodes)
        if test:
            precipMap = self.getTileLayerUrl(accum.visualize(
                min=crange[0], max=crange[1], palette=hexcodes))
        else:
            precipMap = ''

        return precipMap

    # ===================== Surface Water Map ===================== */

    def getSurfaceWaterMap(self, date, sensor):
        sdate = ee.Date(date)
        sensor = sensor
        mekong_region = ee.FeatureCollection('users/kamalhosen/mekong_region')
        aoi = mekong_region.geometry()

        # calculate slope as surface water does usually not occur on slopes
        dem = ee.ImageCollection('JAXA/ALOS/AW3D30/V3_2')
        elevation = dem.select('DSM')

        # Reproject an image mosaic using a projection from one of the image tiles,
        # rather than using the default projection returned by .mosaic().
        proj = elevation.first().select(0).projection()
        slope = ee.Terrain.slope(elevation.mosaic().setDefaultProjection(proj))

        # only include location with historical record of surface water
        jrc = ee.Image(
            "JRC/GSW1_3/GlobalSurfaceWater").select("occurrence").mask()
        jrc = jrc.updateMask(jrc.eq(0))

        slope = slope.updateMask(jrc.eq(0))
        slope = slope.updateMask(slope.gt(5)).gt(0).mask()

        HAND = ee.Image("users/arjenhaag/SERVIR-Mekong/HAND_MERIT")

        th = 50

        if sensor == "sentinel1":
            # Sentinel 1 image collection
            s1Col = ee.ImageCollection("projects/servir-mekong/hydrafloodsSen1").filterBounds(
                aoi).filterDate(sdate.advance(-10, 'day'), sdate.advance(1, 'day'))
            s1 = ee.ImageCollection("COPERNICUS/S1_GRD")

            # get land or water observation from  Sentinel1
            # return 0 = land , 1 = water, mask = nodata
            # sentinel 1 has information on water and land for every pixel, so we only unmask.

            def s1Map(img):
                geomGRD = img.geometry().buffer(-1500)
                mask = ee.Image(s1.filter(ee.Filter.eq(
                    "system:index", img.get("system:index"))).first()).select(0).mask()
                water = ee.Image(img.gt(th).unmask(0)).toInt()
                img = water.set("system:time_start", img.get(
                    "system:time_start")).clip(geomGRD).rename("water")
                return img

            s1Col = s1Col.map(s1Map)

            # sort the collection
            collection = s1Col.sort("system:time_start", False)

            dailywater = collection.reduce(
                ee.Reducer.firstNonNull()).updateMask(slope.eq(0))
            HAND = HAND.updateMask(HAND.gt(40)).gt(0).mask()
            dailywater = dailywater.updateMask(HAND.eq(0)).unmask(0)

            permanentWater = ee.Image(
                "JRC/GSW1_3/GlobalSurfaceWater").select("occurrence").gt(th)
            dailywater = dailywater.selfMask().unmask(
                permanentWater).rename("water").clip(aoi)

        elif sensor == "sentinel2":
            # sentinel 2 image collection
            HF_S2 = ee.ImageCollection("projects/servir-mekong/sentinel2QA").filterBounds(
                aoi).filterDate(sdate.advance(-12, 'day'), sdate.advance(1, 'day'))

            # Create S2 operational single layer
            def s2Map(img):
                geomGRD = img.geometry().buffer(-1500)
                water = img.select("qa").eq(3).unmask(0).toInt()
                img = water.set("system:time_start", img.get(
                    "system:time_start")).clip(geomGRD)
                return img

            HF_S2_tmp = HF_S2.map(s2Map)
            HF_S2_col = HF_S2_tmp.sort("system:time_start", False)

            # Mask with slope & HAND
            HF_S2_tmp = HF_S2_col.reduce(
                ee.Reducer.firstNonNull()).updateMask(slope.eq(0))
            dailywater = HF_S2_tmp.updateMask(HAND.eq(0)).unmask(
                0).selfMask().rename("water").clip(aoi)

        elif sensor == "landsat8":
            # Landsat 8 image collection
            l8Col = ee.ImageCollection("LANDSAT/LC08/C02/T1_RT").filterBounds(
                aoi).filterDate(sdate.advance(-14, 'day'), sdate.advance(1, 'day'))

            # Helper function to extract the values from specific bits
            # The input parameter can be a ee.Number() or ee.Image()
            # Code adapted from https://gis.stackexchange.com/a/349401/5160
            def bitwiseExtract(input, fromBit, toBit):
                maskSize = ee.Number(1).add(toBit).subtract(fromBit)
                mask = ee.Number(1).leftShift(maskSize).subtract(1)
                return input.rightShift(fromBit).bitwiseAnd(mask)

            # sort the collection
            collection = l8Col.sort("system:time_start", False)
            qa = collection.select("QA_PIXEL").reduce(
                ee.Reducer.firstNonNull()).clip(aoi)
            dailywater = bitwiseExtract(qa, 7, 7).eq(1)

            dailywater = dailywater.updateMask(slope.eq(0))
            HAND = HAND.updateMask(HAND.gt(50)).gt(0).mask()
            dailywater = dailywater.updateMask(HAND.eq(0)).unmask(0).selfMask()

        surfaceWaterMap = self.getTileLayerUrl(
            dailywater.visualize(palette="#2389da", min=0, max=1))
        return surfaceWaterMap

    # ===================== Potential Flood Map ===================== */

    def getPotentialFloodMap(self, start_date, end_date, mode, sensor, ops_date):  # adm,
        start_date = start_date
        end_date = end_date
        # adm = adm
        mode = mode
        sensor = sensor
        ops_date = ops_date

        today = datetime.now()
        ops_end_date = ee.Date(today)

        # Exported image collection
        HM = ee.ImageCollection('projects/servir-mekong/HydrafloodsMerge')
        filterHM = ee.Image(HM.filterDate(ops_date, ops_end_date).first())

        # Define pallete color
        p_classes = ['white', '00008b', '33ccff', 'yellow', 'orange', 'red']
        # names_classes = ["No data, Permanent, Seasonal, SAR, Optical, All"]

        # ================ Operational Mode ================= */
        # All Merged
        if mode == "operational" and sensor == "all":
            potentialFloodMap = filterHM.selfMask()
            potentialFloodMap = self.getTileLayerUrl(
                potentialFloodMap.visualize(bands='water', min=0, max=5, palette=p_classes))
            return potentialFloodMap

        # SAR
        elif mode == "operational" and sensor == "sar":
            filterHMSAR = ee.Image(HM.filterDate(
                ops_date, ops_end_date).first().eq(3))
            potentialFloodMap = filterHMSAR.selfMask()
            potentialFloodMap = self.getTileLayerUrl(
                potentialFloodMap.visualize(bands='water', min=0, max=1, palette="yellow"))
            return potentialFloodMap

        # Optical
        elif mode == "operational" and sensor == "optical":
            filterHMOptical = ee.Image(HM.filterDate(
                ops_date, ops_end_date).first().eq(4))
            potentialFloodMap = filterHMOptical.selfMask()
            potentialFloodMap = self.getTileLayerUrl(
                potentialFloodMap.visualize(bands='water', min=0, max=1, palette="orange"))
            return potentialFloodMap

        # SAR + Optical
        elif mode == "operational" and sensor == "sar-optical":
            filterHMSAROptical = ee.Image(HM.filterDate(
                ops_date, ops_end_date).first().eq(5))
            potentialFloodMap = filterHMSAROptical.selfMask()
            potentialFloodMap = self.getTileLayerUrl(
                potentialFloodMap.visualize(bands='water', min=0, max=1, palette="red"))
            return potentialFloodMap

        # ================ Historical Mode ================= */

        # Import study area of LMB
        aoi = ee.FeatureCollection(
            'projects/servir-mekong/Boundary/mekong_region').geometry()

        # Import all image ccollection
        HF_S1 = ee.ImageCollection("projects/servir-mekong/hydrafloodsSen1")
        HF_S2 = ee.ImageCollection("projects/servir-mekong/sentinel2QA")
        HF_L8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_RT")
        S1 = ee.ImageCollection("COPERNICUS/S1_GRD")
        JRC_water = ee.Image("JRC/GSW1_3/GlobalSurfaceWater")
        JRC_monthly = ee.ImageCollection("JRC/GSW1_3/MonthlyHistory")

        # get current date
        cdate = date.today()
        date_time_curr = ee.Date(cdate.strftime("%Y-%m-%d"))
        date_curr = ee.Date.fromYMD(date_time_curr.get(
            'year'), date_time_curr.get('month'), date_time_curr.get('day'))

        # initial date before today
        days_before = 1  # usually 1 before works, sometimes 2 is needed

        # Sentinel-1
        # S1 historical imagery is in [0-100] probability of water
        S1_prob_thresh = 40

        # Sentinel-2 / Landsat 8
        QA_class_values = [0, 1, 2, 3, 4]
        QA_class_names = ['cloud', 'shadow', 'snow', 'water', 'land']
        QA_water_val = 3

        # permanent/seasonal water
        JRC_perm_thresh = 80  # threshold for permanent water from overall JRC occurrence
        # nr of months before and after flood map to use for seasonal water
        JRC_months_spread = 1
        JRC_years_before = 10  # nr of years before current flood map to use for seasonal water
        JRC_seas_thresh = 0.75  # threshold for seasonal water from mean of seasonal images

        # get permanent water
        perm_water = JRC_water.select('occurrence').gte(JRC_perm_thresh)

        # only include location with historical record of surface water
        jrc = ee.Image(
            "JRC/GSW1_3/GlobalSurfaceWater").select("occurrence").mask()
        jrc = jrc.updateMask(jrc.eq(0))

        # Get slope to mask surface water does usually not occur on slopes
        elevation = ee.ImageCollection('JAXA/ALOS/AW3D30/V3_2').select('DSM')

        # Reproject an image mosaic using a projection from one of the image tiles,
        # rather than using the default projection returned by .mosaic().
        proj = elevation.first().select(0).projection()
        slope = ee.Terrain.slope(elevation.mosaic().setDefaultProjection(proj))

        # DEM Mask layer
        slope = slope.updateMask(jrc.eq(0))
        slope = slope.updateMask(slope.gt(5)).gt(0).mask()

        HAND = ee.Image("users/arjenhaag/SERVIR-Mekong/HAND_MERIT")
        HAND = HAND.updateMask(HAND.gt(50)).gt(0).mask()

        # raw imagery
        S1 = S1.filterBounds(aoi).filterDate(start_date, date_curr)

        # JRC permanent water mask to seperate flooded water from surface water for individual sensor
        waterOcc = JRC_water.select('occurrence')
        jrc_data0 = ee.Image("JRC/GSW1_3/Metadata").select('total_obs').lte(0)
        waterOccFilled = waterOcc.unmask(0).max(jrc_data0)
        waterMask = waterOccFilled.lt(40)

        # ---------------------------------------------------------------------------------------------------- //
        # Functions
        # ---------------------------------------------------------------------------------------------------- //

        # seasonal water
        def getSeasonal(date):
            JRC_seasonal = JRC_monthly.filter(ee.Filter.gte('month', date_curr.get('month').subtract(JRC_months_spread)))\
                .filter(ee.Filter.lte('month', date_curr.get('month').add(JRC_months_spread)))\
                .filter(ee.Filter.lte('year', date_curr.get('year')))\
                .filter(ee.Filter.gte('year', date_curr.get('year').subtract(JRC_years_before)))\


            def jrcSeasonalMap(img):
                return img.updateMask(img).remap([1, 2], [0, 1])

            JRC_seasonal = JRC_seasonal.map(jrcSeasonalMap)
            seasonal_water = JRC_seasonal.mean().gte(JRC_seas_thresh)
            return seasonal_water

        def getRefereceWater(date):
            seasonal_water = getSeasonal(date)
            ref_water = seasonal_water.selfMask().add(
                1).unmask().where(perm_water.unmask(), 1)
            ref_water_mask = perm_water.unmask().Or(seasonal_water.unmask())
            return seasonal_water.rename('seasonal_water')\
                .addBands(perm_water.rename('permanent_water'))\
                .addBands(ref_water.rename('reference_water'))\
                .addBands(ref_water_mask.rename('reference_water_mask'))

        HF_S1_tmp = HF_S1.filterBounds(aoi).filterDate(start_date, end_date)
        HF_S2_tmp = HF_S2.filterBounds(aoi).filterDate(start_date, end_date)
        HF_L8_tmp = HF_L8.filterDate(start_date, end_date)

        # To add DOY in Image
        def dateMap(img):
            time = ee.Image(ee.Number.parse(
                ee.Date(img.get("system:time_start")).format("D"))).toFloat().rename("date")
            return img.addBands(time)

        # Create S1 operational single layer
        # get land or water observation from  Sentinel1
        # return 0 = land , 1 = water, mask = nodata
        # sentinel 1 has information on water and land for every pixel, so we only unmask.
        def s1Map(img):
            geomGRD = img.geometry().buffer(-1500)
            mask = ee.Image(S1.filter(ee.Filter.eq(
                "system:index", img.get("system:index"))).first()).select(0).mask()
            water = ee.Image(img.gt(60).unmask(0)).toInt()
            img = water.set("system:time_start", img.get(
                "system:time_start")).clip(geomGRD)
            return img

        HF_S1_tmp = HF_S1_tmp.map(s1Map)
        HF_S1_col = HF_S1_tmp.sort("system:time_start", False)

        # Mask with slope & HAND
        HF_S1_tmp = HF_S1_col.reduce(
            ee.Reducer.firstNonNull()).updateMask(slope.eq(0))
        HF_S1_tmp = HF_S1_tmp.updateMask(HAND.eq(0)).unmask(0).rename("water")

        # Create DOY
        s1_dateCol = HF_S1_col.map(dateMap)
        s1_doy = s1_dateCol.select('date').reduce(
            ee.Reducer.firstNonNull()).rename("DOY")
        HF_S1_tmp = HF_S1_tmp.addBands(s1_doy).toInt().clip(aoi)

        # Create S2 operational single layer
        def s2Map(img):
            geomGRD = img.geometry().buffer(-1500)
            water = img.select("qa").eq(3).unmask(0).toInt()
            img = water.set("system:time_start", img.get(
                "system:time_start")).clip(geomGRD)
            return img

        HF_S2_tmp = HF_S2_tmp.map(s2Map)
        HF_S2_col = HF_S2_tmp.sort("system:time_start", False)

        # Mask with slope & HAND
        HF_S2_tmp = HF_S2_col.reduce(
            ee.Reducer.firstNonNull()).updateMask(slope.eq(0))
        HF_S2_tmp = HF_S2_tmp.updateMask(HAND.eq(0)).unmask(0).rename("water")

        # Create DOY
        s2_dateCol = HF_S2_col.map(dateMap)
        s2_doy = s2_dateCol.select('date').reduce(
            ee.Reducer.firstNonNull()).rename("DOY")
        HF_S2_tmp = HF_S2_tmp.addBands(s2_doy).toInt().clip(aoi)

        # Create L8 operational single layer
        # Helper function to extract the values from specific bits
        # The input parameter can be a ee.Number() or ee.Image()
        # Code adapted from https://gis.stackexchange.com/a/349401/5160
        def bitwiseExtract(input, fromBit, toBit):
            maskSize = ee.Number(1).add(toBit).subtract(fromBit)
            mask = ee.Number(1).leftShift(maskSize).subtract(1)
            return input.rightShift(fromBit).bitwiseAnd(mask)

        # sort the collection
        HF_L8_col = HF_L8_tmp.sort("system:time_start", False)
        qa = HF_L8_col.select("QA_PIXEL").reduce(
            ee.Reducer.firstNonNull()).clip(aoi)
        HF_L8_tmp = bitwiseExtract(qa, 7, 7).eq(1)

        # Mask with slope & HAND
        HF_L8_tmp = HF_L8_tmp.updateMask(slope.eq(0))
        HF_L8_tmp = HF_L8_tmp.updateMask(
            HAND.eq(0)).unmask(0).selfMask().rename("water")

        # Create DoY
        l8_dateCol = HF_L8_col.map(dateMap)
        l8_doy = l8_dateCol.select('date').reduce(
            ee.Reducer.firstNonNull()).rename("DOY")
        HF_L8_tmp = HF_L8_tmp.addBands(l8_doy).toInt().clip(aoi)

        # get seasonal and reference water
        ref_water_all = getRefereceWater(date_curr)

        # merge HYDRAFloods maps
        HF = HF_S1_tmp.select('water').multiply(3)
        HF = HF.unmask(0, False).where(HF_S2_tmp.select('water').unmask(
            0).Or(HF_L8_tmp.select('water').unmask(0)), 4)
        HF = HF.unmask(0, False).where(HF_S1_tmp.select('water').unmask(0).And(
            HF_S2_tmp.select('water').unmask(0).Or(HF_L8_tmp.select('water').unmask(0))), 5)
        HF = HF.unmask(0, False).where(
            ref_water_all.select('seasonal_water').unmask(), 2)
        HF = HF.unmask(0, False).where(ref_water_all.select(
            'permanent_water').unmask(), 1).clip(aoi)

        # All Merged
        if mode == "historical" and sensor == "all":
            potentialFloodMap = HF.selfMask().clip(aoi)
            potentialFloodMap = self.getTileLayerUrl(
                potentialFloodMap.visualize(bands='water', min=0, max=5, palette=p_classes))
            return potentialFloodMap

        elif mode == "historical" and sensor == "sar":
            HF = HF.eq(3)
            potentialFloodMap = HF.selfMask()
            potentialFloodMap = self.getTileLayerUrl(
                potentialFloodMap.visualize(bands='water', min=0, max=1, palette="yellow"))
            return potentialFloodMap

        elif mode == "historical" and sensor == "optical":
            HF = HF.eq(4)
            potentialFloodMap = HF.selfMask()
            potentialFloodMap = self.getTileLayerUrl(
                potentialFloodMap.visualize(bands='water',  min=0, max=1, palette="orange"))
            return potentialFloodMap

        elif mode == "historical" and sensor == "sar-optical":
            HF = HF.eq(5)
            potentialFloodMap = HF.selfMask()
            potentialFloodMap = self.getTileLayerUrl(
                potentialFloodMap.visualize(bands='water',  min=0, max=1, palette="red"))
            return potentialFloodMap

    # ===================== Flood Age Map ===================== */

    def getFloodAgeMap(self, age_date, age_sensor):  # age_type,
        # age_type = age_type
        age_date = age_date
        age_sensor = age_sensor
        today = datetime.now()
        age_end_date = ee.Date(today)

        # Exported image collection
        HM = ee.ImageCollection('projects/servir-mekong/HydrafloodsMerge')

        palette_age = ['ae017e', 'f768a1', 'fbb4b9', 'feebe2']

        if age_sensor == "all":
            filterHM = ee.Image(HM.filterDate(
                age_date, age_end_date).first().select(1))
            # ['ae017e','f768a1','fbb4b9','feebe2']['#f1eef6','#d0d1e6','#a6bddb','#74a9cf','#2b8cbe','#045a8d']
            floodAgeMap = self.getTileLayerUrl(
                filterHM.visualize(min=0, max=7, palette=palette_age))
            return floodAgeMap
        elif age_sensor == "sar":
            filterHM = ee.Image(HM.filterDate(
                age_date, age_end_date).first().select(1).eq(3))
            # ['ae017e','f768a1','fbb4b9','feebe2']['#f1eef6','#d0d1e6','#a6bddb','#74a9cf','#2b8cbe','#045a8d']
            floodAgeMap = self.getTileLayerUrl(
                filterHM.visualize(min=0, max=7, palette=palette_age))
            return floodAgeMap
        elif age_sensor == "optical":
            filterHM = ee.Image(HM.filterDate(
                age_date, age_end_date).first().select(1).eq(4))
            # ['ae017e','f768a1','fbb4b9','feebe2']['#f1eef6','#d0d1e6','#a6bddb','#74a9cf','#2b8cbe','#045a8d']
            floodAgeMap = self.getTileLayerUrl(
                filterHM.visualize(min=0, max=7, palette=palette_age))
            return floodAgeMap

    # ===================== Flood Duration Map ===================== */
    # Get flood duration map
    def getFloodDurationMap(self):
        #  import data
        HF_S1_daily = ee.ImageCollection(
            "projects/servir-mekong/hydrafloodsS1Daily")
        # print(HF_S1_daily.getInfo())

        # system properties
        sys_props = ['system:time_start', 'system:index', 'system:footprint']

        # get latest HYDRAFloods maps
        HF_S1_daily_latest = HF_S1_daily.sort(
            'system:time_start', False).first()
        # print(HF_S1_daily_latest.date());

        # calculate duration
        def calcDuration(curr, prev):
            curr = ee.Image(curr)
            prev_2 = ee.Image(ee.ImageCollection(prev).reduce(ee.Reducer.last())).rename(
                'pwater_mask').cast({'pwater_mask': 'byte'}, ['pwater_mask'])
            duration = ee.Image(prev_2.add(curr)).multiply(curr).cast(
                {'pwater_mask': 'byte'}, ['pwater_mask']).copyProperties(curr, sys_props)
            return ee.ImageCollection(prev).merge(ee.ImageCollection(ee.Image(duration)))

        HF_S1_daily_for_duration = HF_S1_daily.filterDate(HF_S1_daily_latest.date(
        ).advance(-2, 'month'), HF_S1_daily_latest.date().advance(1, 'day'))
        HF_S1_daily_for_duration_first = HF_S1_daily_for_duration.first()
        HF_S1_daily_for_duration_all_except_first = HF_S1_daily_for_duration.filterDate(
            HF_S1_daily_for_duration.first().date().advance(1, 'day'), HF_S1_daily_latest.date().advance(1, 'day'))
        # print(HF_S1_daily_for_duration.size());
        HF_S1_duration = ee.ImageCollection(HF_S1_daily_for_duration_all_except_first.sort('system:time_start').select('pwater_mask').iterate(
            calcDuration, ee.ImageCollection(HF_S1_daily_for_duration_first.select('pwater_mask')))).select(['pwater_mask'], ['duration_days'])
        # print(HF_S1_duration.size())
        HF_S1_daily_duration_latest = HF_S1_duration.sort(
            'system:time_start', False).first()

        image = HF_S1_daily_duration_latest.select('duration_days').selfMask()
        floodDurationMap = self.getTileLayerUrl(
            image.visualize(min=0, max=10, palette=['white', 'black']))  # 'white', 'black'
        return floodDurationMap

    def getDOYMap(self, start_date, end_date):
        start_date = start_date  # datetime.now()#"2022-01-01"
        end_date = end_date
        mekong_region = ee.FeatureCollection('users/kamalhosen/mekong_region')
        aoi = mekong_region.geometry()

        #import image
        s1Col = ee.ImageCollection(
            "projects/servir-mekong/hydrafloodsSen1").filterDate(start_date, end_date)
        s1 = ee.ImageCollection("COPERNICUS/S1_GRD")

        # calculate slope as surface water does usually not occur on slopes
        dem = ee.ImageCollection('JAXA/ALOS/AW3D30/V3_2')
        elevation = dem.select('DSM')

        # Reproject an image mosaic using a projection from one of the image tiles,
        # rather than using the default projection returned by .mosaic().
        proj = elevation.first().select(0).projection()
        slope = ee.Terrain.slope(elevation.mosaic().setDefaultProjection(proj))

        # only include location with historical record of surface water
        jrc = ee.Image(
            "JRC/GSW1_3/GlobalSurfaceWater").select("occurrence").mask()
        jrc = jrc.updateMask(jrc.eq(0))

        slope = slope.updateMask(jrc.eq(0))
        slope = slope.updateMask(slope.gt(5)).gt(0).mask()

        HAND = ee.Image("users/arjenhaag/SERVIR-Mekong/HAND_MERIT")

        th = 50

        # get land or water observation from  Sentinel1
        # return 0 = land , 1 = water, mask = nodata
        # sentinel 1 has information on water and land for every pixel, so we only unmask.

        def s1Map(img):
            geomGRD = img.geometry().buffer(-1500)
            mask = ee.Image(s1.filter(ee.Filter.eq(
                "system:index", img.get("system:index"))).first()).select(0).mask()
            water = ee.Image(img.gt(th).unmask(0)).toInt()
            img = water.set("system:time_start", img.get(
                "system:time_start")).clip(geomGRD).rename("water")
            return img

        s1Col = s1Col.map(s1Map)

        # sort the collection
        collection = s1Col.sort("system:time_start", False)

        dailywater = collection.reduce(
            ee.Reducer.firstNonNull()).updateMask(slope.eq(0)).unmask(0)

        water = ee.Image("JRC/GSW1_2/GlobalSurfaceWater").select("occurrence")
        dailywater = dailywater.updateMask(water)
        dailywater = dailywater.updateMask(dailywater.neq(0))

        permanentWater = ee.Image(
            "JRC/GSW1_3/GlobalSurfaceWater").select("occurrence").gt(th)
        permanentWater = permanentWater.updateMask(permanentWater)
        dailywater = dailywater.updateMask(water).unmask(
            permanentWater).rename("water").clip(aoi)

        # To add DOY in Image
        def dateMap(img):
            time = ee.Image(ee.Number.parse(
                ee.Date(img.get("system:time_start")).format("D"))).toFloat().rename("date")
            return img.addBands(time)

        dateCol = collection.map(dateMap)
        doy = dateCol.select('date').reduce(ee.Reducer.firstNonNull()).rename(
            "DOY").mask(dailywater).clip(aoi)

        # range = doy.reduceRegion(
        #     reducer=ee.Reducer.minMax(),
        #     geometry=aoi,
        #     scale=30,
        #     maxPixels=1e13,
        #     bestEffort=True,
        #     tileScale=16
        # )

        # print("Range:",range)

        # print(dailywater.getInfo())
        doyMap = self.getTileLayerUrl(doy.visualize(min=0, max=120, palette=[
                                      "yellow", "green", "orange", "blue", "red", "purple"]))
        return doyMap

    # -------------------------------------------------------------------------
    def SurfaceWaterAlgorithm(aoi, images, pcnt_perm, pcnt_temp, water_thresh, ndvi_thresh, hand_mask):

        STD_NAMES = ['blue2', 'blue', 'green', 'red', 'nir', 'swir1', 'swir2']

        # calculate percentile images
        prcnt_img_perm = images.reduce(ee.Reducer.percentile(
            [float(pcnt_perm)])).rename(STD_NAMES)
        prcnt_img_temp = images.reduce(ee.Reducer.percentile(
            [float(pcnt_temp)])).rename(STD_NAMES)

        # MNDWI
        MNDWI_perm = prcnt_img_perm.normalizedDifference(['green', 'swir1'])
        MNDWI_temp = prcnt_img_temp.normalizedDifference(['green', 'swir1'])

        # water
        water_perm = MNDWI_perm.gt(float(water_thresh))
        water_temp = MNDWI_temp.gt(float(water_thresh))

        # get NDVI masks
        NDVI_perm_pcnt = prcnt_img_perm.normalizedDifference(['nir', 'red'])
        NDVI_temp_pcnt = prcnt_img_temp.normalizedDifference(['nir', 'red'])
        NDVI_mask_perm = NDVI_perm_pcnt.gt(float(ndvi_thresh))
        NDVI_mask_temp = NDVI_temp_pcnt.gt(float(ndvi_thresh))

        # combined NDVI and HAND masks
        full_mask_perm = NDVI_mask_perm.add(hand_mask)
        full_mask_temp = NDVI_mask_temp.add(hand_mask)

        # apply NDVI and HAND masks
        water_perm_masked = water_perm.updateMask(full_mask_perm.Not())
        water_temp_masked = water_temp.updateMask(full_mask_perm.Not())

        # single image with permanent and temporary water
        water_complete = water_perm_masked.add(water_temp_masked).clip(aoi)

        # return water_complete.updateMask(water_complete)
        return water_complete

    # -------------------------------------------------------------------------
    def getLandsatCollection(aoi, time_start, time_end, month_index=None, climatology=True, defringe=True, cloud_thresh=None):

        # Landsat band names
        LC457_BANDS = ['B1',    'B1',   'B2',    'B3',  'B4',  'B5',    'B7']
        LC8_BANDS = ['B1',    'B2',   'B3',    'B4',  'B5',  'B6',    'B7']
        STD_NAMES = ['blue2', 'blue', 'green', 'red', 'nir', 'swir1', 'swir2']

        # filter Landsat collections on bounds and dates
        L4 = ee.ImageCollection('LANDSAT/LT04/C01/T1_TOA').filterBounds(
            aoi).filterDate(time_start, ee.Date(time_end).advance(1, 'day'))
        L5 = ee.ImageCollection('LANDSAT/LT05/C01/T1_TOA').filterBounds(
            aoi).filterDate(time_start, ee.Date(time_end).advance(1, 'day'))
        L7 = ee.ImageCollection('LANDSAT/LE07/C01/T1_TOA').filterBounds(
            aoi).filterDate(time_start, ee.Date(time_end).advance(1, 'day'))
        L8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA').filterBounds(
            aoi).filterDate(time_start, ee.Date(time_end).advance(1, 'day'))

        # apply cloud masking
        if int(cloud_thresh) >= 0:
            # helper function: cloud busting
            # (https://code.earthengine.google.com/63f075a9e212f6ed4770af44be18a4fe, Ian Housman and Carson Stam)
            def bustClouds(img):
                t = img
                cs = ee.Algorithms.Landsat.simpleCloudScore(
                    img).select('cloud')
                out = img.mask(img.mask().And(
                    cs.lt(ee.Number(int(cloud_thresh)))))
                return out.copyProperties(t)
            # apply cloud busting function
            L4 = L4.map(bustClouds)
            L5 = L5.map(bustClouds)
            L7 = L7.map(bustClouds)
            L8 = L8.map(bustClouds)

        # select bands and rename
        L4 = L4.select(LC457_BANDS, STD_NAMES)
        L5 = L5.select(LC457_BANDS, STD_NAMES)
        L7 = L7.select(LC457_BANDS, STD_NAMES)
        L8 = L8.select(LC8_BANDS, STD_NAMES)

        # apply defringing
        if defringe == 'true':
            # helper function: defringe Landsat 5 and/or 7
            # (https://code.earthengine.google.com/63f075a9e212f6ed4770af44be18a4fe, Bonnie Ruefenacht)
            k = ee.Kernel.fixed(41, 41,
                                [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                                        1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                                        1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                                        1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
                                        1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
                                        1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
                                        1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
                                        1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
                                        1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
                                        1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
                                        1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
                                        1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
                                        1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
                                        1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                                        1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                                        1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                                        1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,
                                        1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,
                                        1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,
                                        1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                                        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                                        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                                        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
            # define number of non null observations for pixel to not be classified as a fringe
            fringeCountThreshold = 279

            def defringeLandsat(img):
                m = img.mask().reduce(ee.Reducer.min())
                sum = m.reduceNeighborhood(ee.Reducer.sum(), k, 'kernel')
                sum = sum.gte(fringeCountThreshold)
                img = img.mask(img.mask().And(sum))
                return img
            L5 = L5.map(defringeLandsat)
            L7 = L7.map(defringeLandsat)

        # merge collections
        images = ee.ImageCollection(L4.merge(L5).merge(L7).merge(L8))

        # filter on selected month
        if climatology:
            if month_index != None:
                images = images.filter(ee.Filter.calendarRange(
                    int(month_index), int(month_index), 'month'))
            else:
                raise ValueError(
                    'Month needs to be defined to calculate climatology')

        return images

    # -------------------------------------------------------------------------
    def JRCAlgorithm(self, startYear, endYear, startMonth, endMonth, method):

        IMAGE_COLLECTION = ee.ImageCollection('JRC/GSW1_3/MonthlyHistory')

        if method == 'discrete':
            myjrc = IMAGE_COLLECTION.filter(ee.Filter.calendarRange(int(startYear), int(endYear), 'year')).\
                filter(ee.Filter.calendarRange(int(startMonth), int(
                    endMonth), 'month'))  # .filterBounds(geom)
        else:
            # filterBounds(geom).
            myjrc = IMAGE_COLLECTION.filterDate(
                startYear + '-' + startMonth, endYear + '-' + endMonth)

        #myjrc = IMAGE_COLLECTION.filterBounds(geom).filterDate(startDate, endDate)

        # if month != None:
        #    myjrc = myjrc.filter(ee.Filter.calendarRange(int(month), int(month), 'month'))

        # calculate total number of observations
        def calcObs(img):
            # observation is img > 0
            obs = img.gt(0)
            return ee.Image(obs).set('system:time_start', img.get('system:time_start'))

        # calculate the number of times water
        def calcWater(img):
            water = img.select('water').eq(2)
            return ee.Image(water).set('system:time_start', img.get('system:time_start'))

        observations = myjrc.map(calcObs)

        water = myjrc.map(calcWater)

        # sum the totals
        totalObs = ee.Image(ee.ImageCollection(observations).sum().toFloat())
        totalWater = ee.Image(ee.ImageCollection(water).sum().toFloat())

        # calculate the percentage of total water
        returnTime = totalWater.divide(totalObs).multiply(100)

        # make a mask
        water = returnTime.gt(75).rename(['water'])
        landShp = ee.FeatureCollection('USDOS/LSIB/2013')
        water = water.updateMask(water).clip(landShp)

        return water

    # -------------------------------------------------------------------------
    def getHistoricalMap(self, startYear, endYear, startMonth, endMonth, method='discrete',
                         climatology=True,
                         month=None,
                         defringe=True,
                         pcnt_perm=40,
                         pcnt_temp=8,
                         water_thresh=0.35,
                         ndvi_thresh=0.5,
                         hand_thresh=30,
                         cloud_thresh=10,
                         algorithm='SWT',
                         wcolor='0000FF',):

        # def spatialSelect(feature):
        #     test = ee.Algorithms.If(geom.contains(feature.geometry()),feature,None)
        #     return ee.Feature(test)

        #countries = landShp.filterBounds(geom).map(spatialSelect,True)
        #self.geom = geom
        #WEST, SOUTH, EAST, NORTH = 92.0, 5, 109.5, 29
        #BOUNDING_BOX = (WEST,SOUTH,EAST,NORTH)
        #self.REGION = ee.Geometry.Rectangle(BOUNDING_BOX)
        # if shape:
        #     shape = shape.replace('["', '[');
        #     shape = shape.replace('"]', ']');
        #     shape = shape.replace('","', ',');
        #     shape = ee.FeatureCollection(eval(shape));
        # else:
        #shape = self.REGION

        mekong_region = ee.FeatureCollection('users/kamalhosen/mekong_region')
        shape = mekong_region.geometry()

        if climatology:
            if month == None:
                raise ValueError(
                    'Month needs to be defined to calculate climatology')

        if algorithm == 'SWT':
            iniTime = '{}-01-01'.format(startYear)
            endTime = '{}-12-31'.format(endYear)
            # get images
            images = self.getLandsatCollection(
                iniTime, endTime, climatology, month, defringe, cloud_thresh)  # geom,

            # Height Above Nearest Drainage (HAND)
            HAND = ee.Image('users/arjenhaag/SERVIR-Mekong/HAND_MERIT')

            # get HAND mask
            HAND_mask = HAND.gt(float(hand_thresh))

            water = self.SurfaceWaterAlgorithm(
                images, pcnt_perm, pcnt_temp, water_thresh, ndvi_thresh, HAND_mask)  # .clip(countries)#geom,
            waterMap = self.getTileLayerUrl(water.updateMask(water.eq(2)).visualize(
                min=0, max=2, palette='#ffffff,#9999ff,' + wcolor))

        elif algorithm == 'JRC':
            water = self.JRCAlgorithm(
                startYear, endYear, startMonth, endMonth, method).clip(shape)
            #water = JRCAlgorithm(geom,iniTime,endTime).clip(countries)
            waterMap = self.getTileLayerUrl(water.visualize(
                min=0, max=1, bands='water', opacity=0.5, palette='#ffffff,' + wcolor))

        else:
            raise NotImplementedError(
                'Selected algorithm string not available. Options are: "SWT" or "JRC"')

        return waterMap

    def _get_geometry(self, shape):

        if shape:
            if shape == 'rectangle':
                _geom = self.geom.split(',')
                coor_list = [float(_geom_) for _geom_ in _geom]
                geometry = ee.Geometry.Rectangle(coor_list)
                return geometry
            elif shape == 'circle':
                _geom = self.center.split(',')
                coor_list = [float(_geom_) for _geom_ in _geom]
                geometry = ee.Geometry.Point(
                    coor_list).buffer(float(self.radius))
                return geometry
            elif shape == 'polygon':
                _geom = self.geom.split(',')
                coor_list = [float(_geom_) for _geom_ in _geom]
                geometry = ee.Geometry.Polygon(coor_list)
                return geometry
            elif shape == 'polyline':
                _geom = self.geom.split(',')
                coor_list = [float(_geom_) for _geom_ in _geom]
                geometry = ee.Geometry.LineString(coor_list)
                return geometry

    # -------------------------------------------------------------------------
    def getDownloadURL(self, date, adm):  # , shape
        return_obj = {}
        try:

            now = date  # datetime.now()#"2022-01-01"
            # mekong_region = ee.FeatureCollection('users/kamalhosen/mekong_region')
            # aoi = mekong_region.geometry()

            lsib = ee.FeatureCollection('USDOS/LSIB/2017')

            adm = adm

            if adm == "all":
                aoi = lsib.filter(ee.Filter.inList(
                    'COUNTRY_NA', ['Vietnam', 'Laos', 'Cambodia', 'Burma', 'Thailand']))
            else:
                aoi = lsib.filter(ee.Filter.eq('COUNTRY_NA', adm))

            #import image
            s1Col = ee.ImageCollection(
                "projects/servir-mekong/hydrafloodsSen1").filterDate("2021-10-05", now)
            s1 = ee.ImageCollection("COPERNICUS/S1_GRD")

            # calculate slope as surface water does usually not occur on slopes
            dem = ee.ImageCollection('JAXA/ALOS/AW3D30/V3_2')
            elevation = dem.select('DSM')

            # Reproject an image mosaic using a projection from one of the image tiles,
            # rather than using the default projection returned by .mosaic().
            proj = elevation.first().select(0).projection()
            slope = ee.Terrain.slope(
                elevation.mosaic().setDefaultProjection(proj))

            # only include location with historical record of surface water
            jrc = ee.Image(
                "JRC/GSW1_3/GlobalSurfaceWater").select("occurrence").mask()
            jrc = jrc.updateMask(jrc.eq(0))

            slope = slope.updateMask(jrc.eq(0))
            slope = slope.updateMask(slope.gt(5)).gt(0).mask()

            HAND = ee.Image("users/arjenhaag/SERVIR-Mekong/HAND_MERIT")

            th = 40

            # get land or water observation from  Sentinel1
            # return 0 = land , 1 = water, mask = nodata
            # sentinel 1 has information on water and land for every pixel, so we only unmask.

            def s1Map(img):
                geomGRD = img.geometry().buffer(-1500)
                mask = ee.Image(s1.filter(ee.Filter.eq(
                    "system:index", img.get("system:index"))).first()).select(0).mask()
                water = ee.Image(img.gt(th).unmask(0)).toInt()
                img = water.set("system:time_start", img.get(
                    "system:time_start")).clip(geomGRD).rename("water")
                return img

            s1Col = s1Col.map(s1Map)

            # sort the collection
            collection = s1Col.sort("system:time_start", False)

            dailywater = collection.reduce(
                ee.Reducer.firstNonNull()).updateMask(slope.eq(0))
            HAND = HAND.updateMask(HAND.gt(40)).gt(0).mask()
            dailywater = dailywater.updateMask(HAND.eq(0)).unmask(0)

            permanentWater = ee.Image(
                "JRC/GSW1_3/GlobalSurfaceWater").select("occurrence").gt(th)
            dailywater = dailywater.selfMask().unmask(
                permanentWater).rename("water").clip(aoi)

            # print(dailywater.getInfo())

            # Get potential flood water
            waterOcc = ee.Image(
                'JRC/GSW1_3/GlobalSurfaceWater').select('occurrence')
            jrc_data0 = ee.Image(
                "JRC/GSW1_3/Metadata").select('total_obs').lte(0)
            waterOccFilled = waterOcc.unmask(0).max(jrc_data0)
            waterMask = waterOccFilled.lt(40)

            potentialFloodMap = dailywater.updateMask(waterMask).selfMask()

            dnldURL = potentialFloodMap.getDownloadURL({
                'name': 'floodmap-'+date,
                        'scale': 10000,
                        'crs': 'EPSG:4326'
            })
            return_obj["url"] = dnldURL
            return_obj["success"] = "success"

        except Exception as e:
            return_obj["error"] = "Error Processing Request. Error: " + str(e)

        return return_obj

    # Get Use Case Map
    def getCaseFloodMap(self, date):
        # sentinel 1 surfacece water map
        image = ee.ImageCollection("projects/servir-mekong/hydrafloodsS1Daily")

        # Flood event date
        date_time_str = date
        event_date = datetime.strptime(date_time_str, '%Y-%m-%d')
        start_date = event_date - timedelta(days=7)
        end_date = event_date + timedelta(days=7)
        #start_date = "2021-10-20"
        #end_date = "2021-10-30"
        #print(start_date, end_date)
        fc = image.filterDate(start_date, end_date).max()
        image = ee.Image(fc.select(0))
        sw_image = image.updateMask(image)

        # JRC Image Collection version GSW1_3
        waterOcc = ee.Image(
            'JRC/GSW1_3/GlobalSurfaceWater').select('occurrence')
        jrc_data0 = ee.Image("JRC/GSW1_3/Metadata").select('total_obs').lte(0)
        waterOccFilled = waterOcc.unmask(0).max(jrc_data0)
        waterMask = waterOccFilled.lt(50)

        onlyFloodImg = sw_image.updateMask(waterMask)

        # startYear = 2000
        # endYear = 2021
        # startMonth = 1
        # endMonth = 12
        # method = 'discrete'
        # permanent_water = self.JRCAlgorithm(startYear, endYear, startMonth, endMonth, method)
        # #print( permanent_water)
        # onlyFloodImg = sw_image.updateMask(permanent_water.not())

        case1FloodMap = self.getTileLayerUrl(
            onlyFloodImg.visualize(palette="#e57373", min=0, max=1))
        return case1FloodMap

    def getJRCPermanentWaterMap(self):
        mekong_region = ee.FeatureCollection('users/kamalhosen/mekong_region')
        shape = mekong_region.geometry()
        waterOcc = ee.Image(
            'JRC/GSW1_3/GlobalSurfaceWater').select('occurrence').clip(shape)
        JRCPermanentMap = self.getTileLayerUrl(waterOcc.visualize(
            palette=['ffffff', 'ffbbbb', '0000ff'], min=0.0, max=100.0))
        return JRCPermanentMap

    def getFloodDepthMap(self, date):
        # date = ee.Date(date)
        date = date
        depth_ic = ee.ImageCollection("projects/servir-mekong/HydrafloodsDepth")
        filterHD = ee.Image(depth_ic.filterDate(date).first())
        # print(filterHD.getInfo())
        if filterHD.getInfo() == None:
            # today = datetime.now().strftime('%Y-%m-%d')
            # today_str = datetime.strptime(today, '%Y-%m-%d')
            # previous_day = today_str - timedelta(days=1)
            # ops_date = previous_day.strftime('%Y%m%d')
            floodmap_collection = ee.ImageCollection(
                "projects/servir-mekong/HydrafloodsMerge")
            filter_floodmap = floodmap_collection.filter(
                ee.Filter.eq('system:index', date)).first()
            curr_floodmap = filter_floodmap.select('water').selfMask()
            flood_depths_calc = hf.depths.fwdet(curr_floodmap.gte(1), ee.Image("MERIT/DEM/v1_0_3")) #.updateMask(curr_floodmap.gte(3))
            depthMap = flood_depths_calc.updateMask(curr_floodmap.gte(3))
        else:
            depthMap = filterHD

        fldDepthMap = self.getTileLayerUrl(depthMap.visualize(
            palette=['FFFFFF', 'ECF0FC', 'B3C3F3', '8DA5ED', '6787E7', '4169E1'], min=0.0, max=5.0))
        return fldDepthMap
