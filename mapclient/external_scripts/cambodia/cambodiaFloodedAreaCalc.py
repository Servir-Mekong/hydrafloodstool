# -*- coding: utf-8 -*-
from datetime import date
from unittest import result
import ee, os, csv
import pandas as pd
ee.Initialize()

# Get list of date from image collection
def getDateList():
  pickup_dict = {}
  def imgDate(d):
    return ee.Date(d).format("YYYY-MM-dd")
  ImageCollection = ee.ImageCollection("projects/servir-mekong/hydrafloodsS1Daily")
  dates = ee.List(ImageCollection.aggregate_array("system:time_start")).map(imgDate).getInfo()
  return dates
dateList = getDateList()

recent_date = dateList[-1]

with open('./static/data/cambodia/cambodia_flooded_area.txt', "a+") as f:
  # Move read cursor to the start of file.
  f.seek(0)
  # If file is not empty then append '\n'
  data = pd.read_csv(f)
  # Get last row 
  lastline = data.tail(1)
  #Get date
  date = lastline['Date'].values[0]
  # print(date)

  if len(data) > 0 and date != recent_date:

    # SERVIR-Mekong sentinel 1 surface water 
    sw = ee.ImageCollection("projects/servir-mekong/hydrafloodsS1Daily")

    # Import country layers
    countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")

    # Filter collection
    fc = sw.filterDate(recent_date)
    filtered_sw = ee.Image(fc.first()).select(0)

    # JRC Image Collection version GSW1_3
    waterOcc = ee.Image('JRC/GSW1_3/GlobalSurfaceWater').select('occurrence')
    jrc_data0 = ee.Image("JRC/GSW1_3/Metadata").select('total_obs').lte(0)
    waterOccFilled = waterOcc.unmask(0).max(jrc_data0)
    waterMask = waterOccFilled.lt(50)

    # Mask surface water layer by JRC permanent water layer
    floodedWater = filtered_sw.updateMask(waterMask)

    ## ======================== Calculate and Save Flooded Water Area for Cambodia ============================ */

    # Select Cambodia
    cambodia = countries.filter(ee.Filter.eq("country_na", "Cambodia"))

    # Clip flood layer to cambodia 
    floodedWaterCambodia = floodedWater.clip(cambodia)
    selectCambodiaFloodedWaterPixel = floodedWaterCambodia.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterCambodia.get('system:time_start')).format('YYYY-MM-dd'))
    #print(selectCambodiaFloodedWaterPixel.getInfo())

    cambodiaFloodedArea = selectCambodiaFloodedWaterPixel.reduceRegion(
      reducer = ee.Reducer.sum(),
      geometry = cambodia.geometry(),
      scale = 10,
      maxPixels = 1e13
    )
    #print(khFloodedAreas.getInfo())
    cambodiaFloodedAreaSqKm = ee.Number(cambodiaFloodedArea.get('water')).divide(1e6).round()
    cambodiaFloodedAreaDate = ee.String(selectCambodiaFloodedWaterPixel.get('date'))
    print(cambodiaFloodedAreaSqKm.getInfo(), cambodiaFloodedAreaDate.getInfo())

    f.write("\n")
    # Append text at the end of file
    output = str(cambodiaFloodedAreaDate.getInfo())+','+ str(cambodiaFloodedAreaSqKm.getInfo())
    f.write(output)
  else: 
    print('Already Calculated')

  ## ======================== End Calculation ============================ */