# -*- coding: utf-8 -*-
from datetime import date
import imghdr
import nntplib
from unittest import result
import ee, os, csv
#ee.Initialize()
service_account = 'hydrafloods@hydrafloods-308007.iam.gserviceaccount.com'
EE_PRIVATE_KEY_FILE = '/home/ubuntu/hydrafloodstool/hydrafloodviewer/credentials/privatekey.json'
credentials = ee.ServiceAccountCredentials(service_account, EE_PRIVATE_KEY_FILE)
ee.Initialize(credentials)

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

## ======================== Calculate and Save number of Flooded Education Center for Cambodia ============================ */

# Select Cambodia
cambodia = countries.filter(ee.Filter.eq("country_na", "Cambodia"))
# Select Cambodia Education
cambodiaEducation = ee.FeatureCollection("users/kamalhosen/servir-mekong/cambodia_education")
#print(cambodiaEducation.size().getInfo())

# Clip flood layer to cambodia 
floodedWaterCambodia = floodedWater.clip(cambodia)
selectCambodiaFloodedWaterPixel = floodedWaterCambodia.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterCambodia.get('system:time_start')).format('YYYY-MM-dd'))
#print(selectCambodiaFloodedWaterPixel.getInfo())

sampleCambodiaEducation = floodedWaterCambodia.unmask(0).sampleRegions(
    collection = cambodiaEducation,
    scale = 100,
    tileScale = 16,
    geometries = True
)  

nonFloodedEduCambodia = sampleCambodiaEducation.filter(ee.Filter.eq("water",0))
floodedEduCambodia = sampleCambodiaEducation.filter(ee.Filter.gt("water",0))

cambodiaNonFloodedEducationCenter = ee.Number(nonFloodedEduCambodia.size())
cambodiaFloodedEducationCenter = ee.Number(floodedEduCambodia.size())
cambodiaFloodedAreaDate = ee.String(selectCambodiaFloodedWaterPixel.get('date'))
#print(cambodiaNonFloodedEducationCenter.getInfo(), cambodiaFloodedEducationCenter.getInfo(), cambodiaFloodedAreaDate.getInfo())

# if os.path.exists('/home/ubuntu/hydrafloodstool/hydrafloodviewer/static/data/cambodia/cambodia_flooded_education_center.txt') == False: 
#   series = "Date,cambodiaFloodedEducationCenter,cambodiaNonFloodedEducationCenter"
#   output = series +'\n'+str(cambodiaFloodedAreaDate.getInfo())+','+ str(cambodiaFloodedEducationCenter.getInfo())+','+str(cambodiaNonFloodedEducationCenter.getInfo())
#   print(output)
# else:
#   print ("Already calculated.")

with open('/home/ubuntu/hydrafloodstool/hydrafloodviewer/static/data/cambodia/cambodia_flooded_education_center.txt', "a+") as f:
  f.seek(0)
  data = f.read(100)
  if len(data) > 0 :
    f.write("\n")
  output = str(cambodiaFloodedAreaDate.getInfo())+','+ str(cambodiaFloodedEducationCenter.getInfo())+','+str(cambodiaNonFloodedEducationCenter.getInfo())
  f.write(output)

## ======================== End Calculation ============================ */

## ======================== Calculate and Save number of Flooded Education Center for Laos ============================ */

# Select Laos
laos = countries.filter(ee.Filter.eq("country_na", "Laos"))
# Select Laos Education
laosEducation = ee.FeatureCollection("users/kamalhosen/servir-mekong/laos_education")
#print(laosEducation.size().getInfo())

# Clip flood layer to laos 
floodedWaterLaos = floodedWater.clip(laos)
selectLaosFloodedWaterPixel = floodedWaterLaos.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterLaos.get('system:time_start')).format('YYYY-MM-dd'))
#print(selectLaosFloodedWaterPixel.getInfo())

sampleLaosEducation = floodedWaterLaos.unmask(0).sampleRegions(
    collection = laosEducation,
    scale = 100,
    tileScale = 16,
    geometries = True
)  

nonFloodedEduLaos = sampleLaosEducation.filter(ee.Filter.eq("water",0))
floodedEduLaos = sampleLaosEducation.filter(ee.Filter.gt("water",0))

laosNonFloodedEducationCenter = ee.Number(nonFloodedEduLaos.size())
laosFloodedEducationCenter = ee.Number(floodedEduLaos.size())
laosFloodedAreaDate = ee.String(selectLaosFloodedWaterPixel.get('date'))
#print(laosNonFloodedEducationCenter.getInfo(), laosFloodedEducationCenter.getInfo(), laosFloodedAreaDate.getInfo())

# if os.path.exists('./static/data/laos/laos_flooded_education_center.txt') == False: 
#   series = "Date,laosFloodedEducationCenter,laosNonFloodedEducationCenter"
#   output = series +'\n'+str(laosFloodedAreaDate.getInfo())+','+ str(laosFloodedEducationCenter.getInfo())+','+str(laosNonFloodedEducationCenter.getInfo())
#   print(output)
# else:
#   print ("Already calculated.")

with open('/home/ubuntu/hydrafloodstool/hydrafloodviewer/static/data/laos/laos_flooded_education_center.txt', "a+") as f:
  f.seek(0)
  data = f.read(100)
  if len(data) > 0 :
    f.write("\n")
  output = str(laosFloodedAreaDate.getInfo())+','+ str(laosFloodedEducationCenter.getInfo())+','+str(laosNonFloodedEducationCenter.getInfo())
  f.write(output)

## ======================== End Calculation ============================ */


## ======================== Calculate and Save number of Flooded Education Center for Myanmar ============================ */

# Select Myanmar
myanmar = countries.filter(ee.Filter.eq("country_na", "Burma"))
# Select Myanmar Education
myanmarEducation = ee.FeatureCollection("users/kamalhosen/servir-mekong/myanmar_education")
#print(myanmarEducation.size().getInfo())

# Clip flood layer to myanmar 
floodedWaterMyanmar = floodedWater.clip(myanmar)
selectMyanmarFloodedWaterPixel = floodedWaterMyanmar.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterMyanmar.get('system:time_start')).format('YYYY-MM-dd'))
#print(selectMyanmarFloodedWaterPixel.getInfo())
sampleMyanmarEducation = floodedWaterMyanmar.unmask(0).sampleRegions(
    collection = myanmarEducation,
    scale = 100,
    tileScale = 16,
    geometries = True
)  

nonFloodedEduMyanmar = sampleMyanmarEducation.filter(ee.Filter.eq("water",0))
floodedEduMyanmar = sampleMyanmarEducation.filter(ee.Filter.gt("water",0))

myanmarNonFloodedEducationCenter = ee.Number(nonFloodedEduMyanmar.size())
myanmarFloodedEducationCenter = ee.Number(floodedEduMyanmar.size())
myanmarFloodedAreaDate = ee.String(selectMyanmarFloodedWaterPixel.get('date'))
#print(myanmarNonFloodedEducationCenter.getInfo(), myanmarFloodedEducationCenter.getInfo(), myanmarFloodedAreaDate.getInfo())

# if os.path.exists('./static/data/myanmar/myanmar_flooded_education_center.txt') == False: 
#   series = "Date,myanmarFloodedEducationCenter,myanmarNonFloodedEducationCenter"
#   output = series +'\n'+str(myanmarFloodedAreaDate.getInfo())+','+ str(myanmarFloodedEducationCenter.getInfo())+','+str(myanmarNonFloodedEducationCenter.getInfo())
#   print(output)
# else:
#   print ("Already calculated.")

with open('/home/ubuntu/hydrafloodstool/hydrafloodviewer/static/data/myanmar/myanmar_flooded_education_center.txt', "a+") as f:
  f.seek(0)
  data = f.read(100)
  if len(data) > 0 :
    f.write("\n")
  output = str(myanmarFloodedAreaDate.getInfo())+','+ str(myanmarFloodedEducationCenter.getInfo())+','+str(myanmarNonFloodedEducationCenter.getInfo())
  f.write(output)

## ======================== End Calculation ============================ */

## ======================== Calculate and Save number of Flooded Education Center for Thailand ============================ */

# Select Thailand
thailand = countries.filter(ee.Filter.eq("country_na", "Thailand"))
# Select Thailand Education
thailandEducation = ee.FeatureCollection("users/kamalhosen/servir-mekong/thailand_education")
#print(thailandEducation.size().getInfo())

# Clip flood layer to thailand 
floodedWaterThailand = floodedWater.clip(thailand)
selectThailandFloodedWaterPixel = floodedWaterThailand.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterThailand.get('system:time_start')).format('YYYY-MM-dd'))
#print(selectThailandFloodedWaterPixel.getInfo())

sampleThailandEducation = floodedWaterThailand.unmask(0).sampleRegions(
    collection = thailandEducation,
    scale = 100,
    tileScale = 16,
    geometries = True
)  

nonFloodedEduThailand = sampleThailandEducation.filter(ee.Filter.eq("water",0))
floodedEduThailand = sampleThailandEducation.filter(ee.Filter.gt("water",0))

thailandNonFloodedEducationCenter = ee.Number(nonFloodedEduThailand.size())
thailandFloodedEducationCenter = ee.Number(floodedEduThailand.size())
thailandFloodedAreaDate = ee.String(selectThailandFloodedWaterPixel.get('date'))
#print(thailandNonFloodedEducationCenter.getInfo(), thailandFloodedEducationCenter.getInfo(), thailandFloodedAreaDate.getInfo())

# if os.path.exists('./static/data/thailand/thailand_flooded_education_center.txt') == False: 
#   series = "Date,thailandFloodedEducationCenter,thailandNonFloodedEducationCenter"
#   output = series +'\n'+str(thailandFloodedAreaDate.getInfo())+','+ str(thailandFloodedEducationCenter.getInfo())+','+str(thailandNonFloodedEducationCenter.getInfo())
#   print(output)
# else:
#   print ("Already calculated.")

with open('/home/ubuntu/hydrafloodstool/hydrafloodviewer/static/data/thailand/thailand_flooded_education_center.txt', "a+") as f:
  f.seek(0)
  data = f.read(100)
  if len(data) > 0 :
    f.write("\n")
  output = str(thailandFloodedAreaDate.getInfo())+','+ str(thailandFloodedEducationCenter.getInfo())+','+str(thailandNonFloodedEducationCenter.getInfo())
  f.write(output)

## ======================== End Calculation ============================ */

## ======================== Calculate and Save number of Flooded Education Center for Vietnam ============================ */

# Select Vietnam
vietnam = countries.filter(ee.Filter.eq("country_na", "Vietnam"))
# Select Vietnam Education
vietnamEducation = ee.FeatureCollection("users/kamalhosen/servir-mekong/vietnam_education")
#print(vietnamEducation.size().getInfo())

# Clip flood layer to vietnam 
floodedWaterVietnam = floodedWater.clip(vietnam)
selectVietnamFloodedWaterPixel = floodedWaterVietnam.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterVietnam.get('system:time_start')).format('YYYY-MM-dd'))
#print(selectVietnamFloodedWaterPixel.getInfo())

sampleVietnamEducation = floodedWaterVietnam.unmask(0).sampleRegions(
    collection = vietnamEducation,
    scale = 100,
    tileScale = 16,
    geometries = True
)  

nonFloodedEduVietnam = sampleVietnamEducation.filter(ee.Filter.eq("water",0))
floodedEduVietnam = sampleVietnamEducation.filter(ee.Filter.gt("water",0))

vietnamNonFloodedEducationCenter = ee.Number(nonFloodedEduVietnam.size())
vietnamFloodedEducationCenter = ee.Number(floodedEduVietnam.size())
vietnamFloodedAreaDate = ee.String(selectVietnamFloodedWaterPixel.get('date'))
#print(vietnamNonFloodedEducationCenter.getInfo(), vietnamFloodedEducationCenter.getInfo(), vietnamFloodedAreaDate.getInfo())

# if os.path.exists('./static/data/vietnam/vietnam_flooded_education_center.txt') == False: 
#   series = "Date,vietnamFloodedEducationCenter,vietnamNonFloodedEducationCenter"
#   output = series +'\n'+str(vietnamFloodedAreaDate.getInfo())+','+ str(vietnamFloodedEducationCenter.getInfo())+','+str(vietnamNonFloodedEducationCenter.getInfo())
#   print(output)
# else:
#   print ("Already calculated.")

with open('/home/ubuntu/hydrafloodstool/hydrafloodviewer/static/data/vietnam/vietnam_flooded_education_center.txt', "a+") as f:
  f.seek(0)
  data = f.read(100)
  if len(data) > 0 :
    f.write("\n")
  output = str(vietnamFloodedAreaDate.getInfo())+','+ str(vietnamFloodedEducationCenter.getInfo())+','+str(vietnamNonFloodedEducationCenter.getInfo())
  f.write(output)

## ======================== End Calculation ============================ */
