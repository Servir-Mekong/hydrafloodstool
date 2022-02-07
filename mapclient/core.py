# -*- coding: utf-8 -*-
from turtle import st
from django.core import serializers
from django.http import HttpResponse
import datetime
import numpy as np
import base64
import matplotlib as mpl
#import feedparser
mpl.use('Agg')
import matplotlib.pyplot as plt
mpl.rcParams.update({'font.size': 14})
from django.conf import settings
import ee, json, os, time
from django.http import JsonResponse
from django.http import HttpResponse
from ee.ee_exception import EEException
from datetime import datetime, timedelta

####/////////////////////////////////////////////
class MainGEEApi():
    #Get list of available dates
    def getDateList(self):
        pickup_dict = {}
        def imgDate(d):
            return ee.Date(d).format("YYYY-MM-dd")
        ImageCollection = ee.ImageCollection("projects/servir-mekong/hydrafloodsS1Daily")
        dates = ee.List(ImageCollection.aggregate_array("system:time_start")).map(imgDate).getInfo()
        return dates

    #Get earth engine tile layer
    def getTileLayerUrl(self, ee_image_object):
        map_id = ee.Image(ee_image_object).getMapId()
        tile_url_template = str(map_id['tile_fetcher'].url_format)
        return tile_url_template

    #Get precipitation map
    def getPrecipMap(self, date, accumulation=1, cmap_name='nipy_spectral'):
        def _accumulate(ic,date,ndays=1):
            eeDate = ee.Date(date)
            ic_filtered = ic.filterDate(eeDate.advance(-(ndays-1),'day'),eeDate.advance(1,'day'))
            accum_img = ee.Image(ic_filtered.sum())
            return accum_img.mask(accum_img.gt(1))

        if int(accumulation) not in [1,3,7]:
            raise NotImplementedError('Selected accumulation value is not yet implemented, options are: 1, 3, 7')

        ic = ee.ImageCollection('JAXA/GPM_L3/GSMaP/v6/operational').select(['hourlyPrecipRateGC'])

        ranges = {1:[1,100],3:[1,250],7:[1,500]}
        crange = ranges[int(accumulation)]

        accum = _accumulate(ic,date,int(accumulation))
        nBands = len(accum.bandNames().getInfo())
        test = nBands > 0

        cmap = mpl.cm.get_cmap(cmap_name, 100)

        hexcodes = []
        for i in range(cmap.N):
           rgb = cmap(i)[:3] # will return rgba, we take only first 3 so we get rgb
           hexcodes.append(mpl.colors.rgb2hex(rgb))
        colormap = ','.join(hexcodes)
        if test:
            precipMap = self.getTileLayerUrl(accum.visualize(min=crange[0],max=crange[1], palette=hexcodes))
        else:
            precipMap = ''

        return precipMap

    #Get surface water map 
    def getSurfaceWaterMap(self, date):
        image = ee.ImageCollection("projects/servir-mekong/hydrafloodsS1Daily")
        fc = image.filterDate(date)  
        # mekong_region = ee.FeatureCollection('users/kamalhosen/mekong_region')
        # shape = mekong_region.geometry()
        image = ee.Image(fc.first()).select(0)#.clip(shape)
        image = image.updateMask(image)
        surfaceWaterMap = self.getTileLayerUrl(image.visualize(palette="#2389da",min=0,max=1))
        return surfaceWaterMap


    # -------------------------------------------------------------------------
    def SurfaceWaterAlgorithm(aoi,images, pcnt_perm, pcnt_temp, water_thresh, ndvi_thresh, hand_mask):

        STD_NAMES   = ['blue2', 'blue', 'green', 'red', 'nir', 'swir1', 'swir2']

        # calculate percentile images
        prcnt_img_perm = images.reduce(ee.Reducer.percentile([float(pcnt_perm)])).rename(STD_NAMES)
        prcnt_img_temp = images.reduce(ee.Reducer.percentile([float(pcnt_temp)])).rename(STD_NAMES)

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

        #return water_complete.updateMask(water_complete)
        return water_complete

    # -------------------------------------------------------------------------
    def getLandsatCollection(aoi,time_start, time_end, month_index=None, climatology=True, defringe=True, cloud_thresh=None):

        # Landsat band names
        LC457_BANDS = ['B1',    'B1',   'B2',    'B3',  'B4',  'B5',    'B7']
        LC8_BANDS   = ['B1',    'B2',   'B3',    'B4',  'B5',  'B6',    'B7']
        STD_NAMES   = ['blue2', 'blue', 'green', 'red', 'nir', 'swir1', 'swir2']

        # filter Landsat collections on bounds and dates
        L4 = ee.ImageCollection('LANDSAT/LT04/C01/T1_TOA').filterBounds(aoi).filterDate(time_start, ee.Date(time_end).advance(1, 'day'))
        L5 = ee.ImageCollection('LANDSAT/LT05/C01/T1_TOA').filterBounds(aoi).filterDate(time_start, ee.Date(time_end).advance(1, 'day'))
        L7 = ee.ImageCollection('LANDSAT/LE07/C01/T1_TOA').filterBounds(aoi).filterDate(time_start, ee.Date(time_end).advance(1, 'day'))
        L8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA').filterBounds(aoi).filterDate(time_start, ee.Date(time_end).advance(1, 'day'))

        # apply cloud masking
        if int(cloud_thresh) >= 0:
            # helper function: cloud busting
            # (https://code.earthengine.google.com/63f075a9e212f6ed4770af44be18a4fe, Ian Housman and Carson Stam)
            def bustClouds(img):
                t = img
                cs = ee.Algorithms.Landsat.simpleCloudScore(img).select('cloud')
                out = img.mask(img.mask().And(cs.lt(ee.Number(int(cloud_thresh)))))
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
            k = ee.Kernel.fixed(41, 41, \
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
            fringeCountThreshold = 279  # define number of non null observations for pixel to not be classified as a fringe
            def defringeLandsat(img):
                m   = img.mask().reduce(ee.Reducer.min())
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
                images = images.filter(ee.Filter.calendarRange(int(month_index), int(month_index), 'month'))
            else:
                raise ValueError('Month needs to be defined to calculate climatology')

        return images

    # -------------------------------------------------------------------------
    def JRCAlgorithm(self, startYear, endYear, startMonth, endMonth, method):

        IMAGE_COLLECTION = ee.ImageCollection('JRC/GSW1_0/MonthlyHistory')

        if method == 'discrete':
            myjrc = IMAGE_COLLECTION.filter(ee.Filter.calendarRange(int(startYear), int(endYear), 'year')).\
                        filter(ee.Filter.calendarRange(int(startMonth), int(endMonth), 'month')) #.filterBounds(geom)
        else:
            myjrc = IMAGE_COLLECTION.filterDate(startYear + '-' + startMonth, endYear + '-' + endMonth)#filterBounds(geom).

        #myjrc = IMAGE_COLLECTION.filterBounds(geom).filterDate(startDate, endDate)

        #if month != None:
        #    myjrc = myjrc.filter(ee.Filter.calendarRange(int(month), int(month), 'month'))

        # calculate total number of observations
        def calcObs(img):
            # observation is img > 0
            obs = img.gt(0);
            return ee.Image(obs).set('system:time_start', img.get('system:time_start'));

        # calculate the number of times water
        def calcWater(img):
            water = img.select('water').eq(2);
            return ee.Image(water).set('system:time_start', img.get('system:time_start'));

        observations = myjrc.map(calcObs)

        water = myjrc.map(calcWater)

        # sum the totals
        totalObs = ee.Image(ee.ImageCollection(observations).sum().toFloat());
        totalWater = ee.Image(ee.ImageCollection(water).sum().toFloat());

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
        wcolor='#00008b',):

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

        mekong_region = ee.FeatureCollection('users/kamalhosen/mekong_region');
        shape = mekong_region.geometry();

        if climatology:
            if month == None:
                raise ValueError('Month needs to be defined to calculate climatology')

        if algorithm == 'SWT':
            iniTime = '{}-01-01'.format(startYear)
            endTime = '{}-12-31'.format(endYear)
            # get images
            images = self.getLandsatCollection(iniTime, endTime, climatology, month, defringe, cloud_thresh)#geom,

            # Height Above Nearest Drainage (HAND)
            HAND = ee.Image('users/arjenhaag/SERVIR-Mekong/HAND_MERIT')

            # get HAND mask
            HAND_mask = HAND.gt(float(hand_thresh))

            water = self.SurfaceWaterAlgorithm(images, pcnt_perm, pcnt_temp, water_thresh, ndvi_thresh, HAND_mask)#.clip(countries)#geom,
            waterMap = self.getTileLayerUrl(water.updateMask(water.eq(2)).visualize(min=0,max=2,palette='#ffffff,#9999ff,'+ wcolor))

        elif algorithm == 'JRC':
            water = self.JRCAlgorithm(startYear, endYear, startMonth, endMonth, method).clip(shape)
            #water = JRCAlgorithm(geom,iniTime,endTime).clip(countries)
            waterMap = self.getTileLayerUrl(water.visualize(min=0,max=1,bands='water',opacity = 0.5, palette='#ffffff,'+ wcolor))

        else:
            raise NotImplementedError('Selected algorithm string not available. Options are: "SWT" or "JRC"')

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
                geometry = ee.Geometry.Point(coor_list).buffer(float(self.radius))
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
    def getDownloadURL(self, date, shape):
        return_obj = {}
        try:
            shape = shape.replace('["', '[');
            shape = shape.replace('"]', ']');
            shape = shape.replace('","', ',');
            shape = ee.FeatureCollection(eval(shape));
            t1 = ee.Date(date)
            t2 = t1.advance(1,'day')
            self.floodExtentCollection = ee.ImageCollection("projects/servir-mekong/hydrafloodsS1Daily")
            fc = self.floodExtentCollection.filterDate(t1,t2) #.filter(ee.Filter.eq('sensor',snsr))
            image = ee.Image(fc.first()).select(0)
            clip_image = image.clip(shape.geometry().dissolve())

            dnldURL = clip_image.getDownloadURL({
                'name': 'floodmap-'+date, 
        		'scale': 90,
        		'crs': 'EPSG:4326'
            })
            return_obj["url"] = dnldURL
            return_obj["success"] = "success"

        except Exception as e:
            return_obj["error"] = "Error Processing Request. Error: "+ str(e)

        return return_obj

    #Get Use Case Map
    def getCaseFloodMap(self, date):
        #sentinel 1 surfacece water map
        image = ee.ImageCollection("projects/servir-mekong/hydrafloodsS1Daily")
        
        #Flood event date
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

        #JRC Image Collection version GSW1_3
        waterOcc = ee.Image('JRC/GSW1_3/GlobalSurfaceWater').select('occurrence')
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

        case1FloodMap = self.getTileLayerUrl(onlyFloodImg.visualize(palette="#e57373",min=0,max=1))
        return case1FloodMap

    def getJRCPermanentWaterMap(self):
        mekong_region = ee.FeatureCollection('users/kamalhosen/mekong_region')
        shape = mekong_region.geometry()
        waterOcc = ee.Image('JRC/GSW1_3/GlobalSurfaceWater').select('occurrence').clip(shape)
        JRCPermanentMap = self.getTileLayerUrl( waterOcc.visualize(palette=['ffffff', 'ffbbbb', '0000ff'], min=0.0, max=100.0) )
        return JRCPermanentMap

    #Get Potential Flood Map
    def getPotentialFloodMap(self, date):
        #sentinel 1 surfacece water map
        image = ee.ImageCollection("projects/servir-mekong/hydrafloodsS1Daily")
        fc = image.filterDate(date)
        image = ee.Image(fc.first()).select(0)
        sw_image = image.updateMask(image)

        #JRC Image Collection version GSW1_3
        waterOcc = ee.Image('JRC/GSW1_3/GlobalSurfaceWater').select('occurrence')
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

        potentialFloodMap = self.getTileLayerUrl(onlyFloodImg.visualize(palette="#e57373",min=0,max=1))
        return potentialFloodMap

    