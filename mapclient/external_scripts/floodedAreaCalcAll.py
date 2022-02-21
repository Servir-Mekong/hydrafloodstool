# -*- coding: utf-8 -*-
from datetime import date
from unittest import result
import ee, os, csv
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
#print(cambodiaFloodedAreaSqKm.getInfo(), cambodiaFloodedAreaDate.getInfo())

if os.path.exists('./static/data/cambodia_flooded_area.txt') == False: 
  series = "Date,TotalAreainSqKm"
  output = series +'\n'+str(cambodiaFloodedAreaDate.getInfo())+','+ str(cambodiaFloodedAreaSqKm.getInfo())
  print(output)
else:
  print ("Already calculated.")

with open('./static/data/cambodia_flooded_area.txt', "a+") as f:
  # Move read cursor to the start of file.
  f.seek(0)
  # If file is not empty then append '\n'
  data = f.read(100)
  if len(data) > 0 :
      f.write("\n")
  # Append text at the end of file
  output = str(cambodiaFloodedAreaDate.getInfo())+','+ str(cambodiaFloodedAreaSqKm.getInfo())
  f.write(output)

## ======================== End Calculation ============================ */


## ======================== Calculate and Save Flooded Water Area for Laos ============================ */

# Select Laos
laos = countries.filter(ee.Filter.eq("country_na", "Laos"))

# Clip flood layer to laos 
floodedWaterLaos = floodedWater.clip(laos)
selectLaosFloodedWaterPixel = floodedWaterLaos.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterLaos.get('system:time_start')).format('YYYY-MM-dd'))
#print(selectLaosFloodedWaterPixel.getInfo())

laosFloodedArea = selectLaosFloodedWaterPixel.reduceRegion(
  reducer = ee.Reducer.sum(),
  geometry = laos.geometry(),
  scale = 10,
  maxPixels = 1e13
)
#print(khFloodedAreas.getInfo())
laosFloodedAreaSqKm = ee.Number(laosFloodedArea.get('water')).divide(1e6).round()
laosFloodedAreaDate = ee.String(selectLaosFloodedWaterPixel.get('date'))
print(laosFloodedAreaSqKm.getInfo(), laosFloodedAreaDate.getInfo())

if os.path.exists('./static/data/laos_flooded_area.txt') == False: 
  series = "Date,TotalAreainSqKm"
  output = series +'\n'+str(laosFloodedAreaDate.getInfo())+','+ str(laosFloodedAreaSqKm.getInfo())
  print(output)
else:
  print ("Already calculated.")

with open('./static/data/laos_flooded_area.txt', "a+") as f:
  # Move read cursor to the start of file.
  f.seek(0)
  # If file is not empty then append '\n'
  data = f.read(100)
  if len(data) > 0 :
      f.write("\n")
  # Append text at the end of file
  output = str(laosFloodedAreaDate.getInfo())+','+ str(laosFloodedAreaSqKm.getInfo())
  f.write(output)

## ======================== End Calculation ============================ */

## ======================== Calculate and Save Flooded Water Area for Myanmar ============================ */

# Select Myanmar
myanmar = countries.filter(ee.Filter.eq("country_na", "Burma"))

# Clip flood layer to myanmar 
floodedWaterMyanmar = floodedWater.clip(myanmar)
selectMyanmarFloodedWaterPixel = floodedWaterMyanmar.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterMyanmar.get('system:time_start')).format('YYYY-MM-dd'))
#print(selectMyanmarFloodedWaterPixel.getInfo())

myanmarFloodedArea = selectMyanmarFloodedWaterPixel.reduceRegion(
  reducer = ee.Reducer.sum(),
  geometry = myanmar.geometry(),
  scale = 30,
  maxPixels = 1e13
)
#print(khFloodedAreas.getInfo())
myanmarFloodedAreaSqKm = ee.Number(myanmarFloodedArea.get('water')).divide(1e6).round()
myanmarFloodedAreaDate = ee.String(selectMyanmarFloodedWaterPixel.get('date'))
print(myanmarFloodedAreaSqKm.getInfo(), myanmarFloodedAreaDate.getInfo())

if os.path.exists('./static/data/myanmar_flooded_area.txt') == False: 
  series = "Date,TotalAreainSqKm"
  output = series +'\n'+str(myanmarFloodedAreaDate.getInfo())+','+ str(myanmarFloodedAreaSqKm.getInfo())
  print(output)
else:
  print ("Already calculated.")

with open('./static/data/myanmar_flooded_area.txt', "a+") as f:
  # Move read cursor to the start of file.
  f.seek(0)
  # If file is not empty then append '\n'
  data = f.read(100)
  if len(data) > 0 :
      f.write("\n")
  # Append text at the end of file
  output = str(myanmarFloodedAreaDate.getInfo())+','+ str(myanmarFloodedAreaSqKm.getInfo())
  f.write(output)

## ======================== End Calculation ============================ */


## ======================== Calculate and Save Flooded Water Area for Thailand ============================ */

# Select Thailand
thailand = countries.filter(ee.Filter.eq("country_na", "Thailand"))

# Clip flood layer to thailand 
floodedWaterThailand = floodedWater.clip(thailand)
selectThailandFloodedWaterPixel = floodedWaterThailand.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterThailand.get('system:time_start')).format('YYYY-MM-dd'))
#print(selectThailandFloodedWaterPixel.getInfo())

thailandFloodedArea = selectThailandFloodedWaterPixel.reduceRegion(
  reducer = ee.Reducer.sum(),
  geometry = thailand.geometry(),
  scale = 30,
  maxPixels = 1e13
)
#print(khFloodedAreas.getInfo())
thailandFloodedAreaSqKm = ee.Number(thailandFloodedArea.get('water')).divide(1e6).round()
thailandFloodedAreaDate = ee.String(selectThailandFloodedWaterPixel.get('date'))
print(thailandFloodedAreaSqKm.getInfo(), thailandFloodedAreaDate.getInfo())

if os.path.exists('./static/data/thailand_flooded_area.txt') == False: 
  series = "Date,TotalAreainSqKm"
  output = series +'\n'+str(thailandFloodedAreaDate.getInfo())+','+ str(thailandFloodedAreaSqKm.getInfo())
  print(output)
else:
  print ("Already calculated.")

with open('./static/data/thailand_flooded_area.txt', "a+") as f:
  # Move read cursor to the start of file.
  f.seek(0)
  # If file is not empty then append '\n'
  data = f.read(100)
  if len(data) > 0 :
      f.write("\n")
  # Append text at the end of file
  output = str(thailandFloodedAreaDate.getInfo())+','+ str(thailandFloodedAreaSqKm.getInfo())
  f.write(output)

## ======================== End Calculation ============================ */


## ======================== Calculate and Save Flooded Water Area for Vietnam ============================ */

# Select Vietnam
vietnam = countries.filter(ee.Filter.eq("country_na", "Vietnam"))

# Clip flood layer to vietnam 
floodedWaterVietnam = floodedWater.clip(vietnam)
selectVietnamFloodedWaterPixel = floodedWaterVietnam.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterVietnam.get('system:time_start')).format('YYYY-MM-dd'))
#print(selectVietnamFloodedWaterPixel.getInfo())

vietnamFloodedArea = selectVietnamFloodedWaterPixel.reduceRegion(
  reducer = ee.Reducer.sum(),
  geometry = vietnam.geometry(),
  scale = 30,
  maxPixels = 1e13
)
#print(khFloodedAreas.getInfo())
vietnamFloodedAreaSqKm = ee.Number(vietnamFloodedArea.get('water')).divide(1e6).round()
vietnamFloodedAreaDate = ee.String(selectVietnamFloodedWaterPixel.get('date'))
print(vietnamFloodedAreaSqKm.getInfo(), vietnamFloodedAreaDate.getInfo())

if os.path.exists('./static/data/vietnam_flooded_area.txt') == False: 
  series = "Date,TotalAreainSqKm"
  output = series +'\n'+str(vietnamFloodedAreaDate.getInfo())+','+ str(vietnamFloodedAreaSqKm.getInfo())
  print(output)
else:
  print ("Already calculated.")

with open('./static/data/vietnam_flooded_area.txt', "a+") as f:
  # Move read cursor to the start of file.
  f.seek(0)
  # If file is not empty then append '\n'
  data = f.read(100)
  if len(data) > 0 :
      f.write("\n")
  # Append text at the end of file
  output = str(vietnamFloodedAreaDate.getInfo())+','+ str(vietnamFloodedAreaSqKm.getInfo())
  f.write(output)

## ======================== End Calculation ============================ */

