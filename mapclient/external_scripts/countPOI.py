# -*- coding: utf-8 -*-
from datetime import date
import imghdr
import nntplib
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

## ======================== Calculate and Save number of Flooded Health Center for Cambodia ============================ */

# Select Cambodia
cambodia = countries.filter(ee.Filter.eq("country_na", "Cambodia"))
cambodiaHospital = ee.FeatureCollection("users/kamalhosen/servir-mekong/cambodia_hospital")
#print(cambodiaHospital.size().getInfo())
# Clip flood layer to cambodia 
floodedWaterCambodia = floodedWater.clip(cambodia)
selectCambodiaFloodedWaterPixel = floodedWaterCambodia.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterCambodia.get('system:time_start')).format('YYYY-MM-dd'))
#print(selectCambodiaFloodedWaterPixel.getInfo())

sampleHospitalCambodia = floodedWaterCambodia.unmask(0).sampleRegions(
    collection = cambodiaHospital,
    scale = 100,
    tileScale = 16,
    geometries = True
)  
#print(sampleHospital)
nonFloodedHospitalCambodia = sampleHospitalCambodia.filter(ee.Filter.eq("water",0))
floodedHospitalCambodia = sampleHospitalCambodia.filter(ee.Filter.gt("water",0))

cambodiaNonFloodedHealthCenter = ee.Number(nonFloodedHospitalCambodia.size())
cambodiaFloodedHealthCenter = ee.Number(floodedHospitalCambodia.size())
cambodiaFloodedAreaDate = ee.String(selectCambodiaFloodedWaterPixel.get('date'))
print(cambodiaNonFloodedHealthCenter.getInfo(), cambodiaFloodedHealthCenter.getInfo(), cambodiaFloodedAreaDate.getInfo())

# if os.path.exists('./static/data/cambodia/cambodia_flooded_health_center.txt') == False: 
#   series = "Date,cambodiaFloodedHealthCenter,cambodiaNonFloodedHealthCenter"
#   output = series +'\n'+str(cambodiaFloodedAreaDate.getInfo())+','+ str(cambodiaFloodedHealthCenter.getInfo())+','+str(cambodiaNonFloodedHealthCenter.getInfo())
#   print(output)
# else:
#   print ("Already calculated.")

with open('./static/data/cambodia/cambodia_flooded_health_center.txt', "a+") as f:
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
    f.write("\n")
    # Append text at the end of file
    output = str(cambodiaFloodedAreaDate.getInfo())+','+ str(cambodiaFloodedHealthCenter.getInfo())+','+str(cambodiaNonFloodedHealthCenter.getInfo())
    f.write(output)
  else:
    print('Already Calculated') 
  

## ======================== End Calculation ============================ */

## ======================== Calculate and Save number of Flooded Health Center for Laos ============================ */

# Select Laos
laos = countries.filter(ee.Filter.eq("country_na", "Laos"))
laosHospital = ee.FeatureCollection("users/kamalhosen/servir-mekong/laos_hospital")
#print(laosHospital.size().getInfo())
# Clip flood layer to laos 
floodedWaterLaos = floodedWater.clip(laos)
selectLaosFloodedWaterPixel = floodedWaterLaos.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterLaos.get('system:time_start')).format('YYYY-MM-dd'))
#print(selectLaosFloodedWaterPixel.getInfo())

sampleHospitalLaos = floodedWaterLaos.unmask(0).sampleRegions(
    collection = laosHospital,
    scale = 100,
    tileScale = 16,
    geometries = True
)  
#print(sampleHospital)
nonFloodedHospitalLaos = sampleHospitalLaos.filter(ee.Filter.eq("water",0))
floodedHospitalLaos = sampleHospitalLaos.filter(ee.Filter.gt("water",0))

laosNonFloodedHealthCenter = ee.Number(nonFloodedHospitalLaos.size())
laosFloodedHealthCenter = ee.Number(floodedHospitalLaos.size())
laosFloodedAreaDate = ee.String(selectLaosFloodedWaterPixel.get('date'))
print(laosNonFloodedHealthCenter.getInfo(), laosFloodedHealthCenter.getInfo(), laosFloodedAreaDate.getInfo())

# if os.path.exists('./static/data/laos/laos_flooded_health_center.txt') == False: 
#   series = "Date,laosFloodedHealthCenter,laosNonFloodedHealthCenter"
#   output = series +'\n'+str(laosFloodedAreaDate.getInfo())+','+ str(laosFloodedHealthCenter.getInfo())+','+str(laosNonFloodedHealthCenter.getInfo())
#   print(output)
# else:
#   print ("Already calculated.")

with open('./static/data/laos/laos_flooded_health_center.txt', "a+") as f:
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
    f.write("\n")
    # Append text at the end of file
    output = str(laosFloodedAreaDate.getInfo())+','+ str(laosFloodedHealthCenter.getInfo())+','+str(laosNonFloodedHealthCenter.getInfo())
    f.write(output)
  else:
    print('Already Calculated') 

## ======================== End Calculation ============================ */

## ======================== Calculate and Save number of Flooded Health Center for Myanmar ============================ */

# Select Myanmar
myanmar = countries.filter(ee.Filter.eq("country_na", "Burma"))
myanmarHospital = ee.FeatureCollection("users/kamalhosen/servir-mekong/myanmar_hospital")
#print(myanmarHospital.size().getInfo())
# Clip flood layer to myanmar 
floodedWaterMyanmar = floodedWater.clip(myanmar)
selectMyanmarFloodedWaterPixel = floodedWaterMyanmar.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterMyanmar.get('system:time_start')).format('YYYY-MM-dd'))
#print(selectMyanmarFloodedWaterPixel.getInfo())

sampleHospitalMyanmar = floodedWaterMyanmar.unmask(0).sampleRegions(
    collection = myanmarHospital,
    scale = 100,
    tileScale = 16,
    geometries = True
)  
#print(sampleHospital)
nonFloodedHospitalMyanmar = sampleHospitalMyanmar.filter(ee.Filter.eq("water",0))
floodedHospitalMyanmar = sampleHospitalMyanmar.filter(ee.Filter.gt("water",0))

myanmarNonFloodedHealthCenter = ee.Number(nonFloodedHospitalMyanmar.size())
myanmarFloodedHealthCenter = ee.Number(floodedHospitalMyanmar.size())
myanmarFloodedAreaDate = ee.String(selectMyanmarFloodedWaterPixel.get('date'))
print(myanmarNonFloodedHealthCenter.getInfo(), myanmarFloodedHealthCenter.getInfo(), myanmarFloodedAreaDate.getInfo())

# if os.path.exists('./static/data/myanmar/myanmar_flooded_health_center.txt') == False: 
#   series = "Date,myanmarFloodedHealthCenter,myanmarNonFloodedHealthCenter"
#   output = series +'\n'+str(myanmarFloodedAreaDate.getInfo())+','+ str(myanmarFloodedHealthCenter.getInfo())+','+str(myanmarNonFloodedHealthCenter.getInfo())
#   print(output)
# else:
#   print ("Already calculated.")

with open('./static/data/myanmar/myanmar_flooded_health_center.txt', "a+") as f:
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
    f.write("\n")
    # Append text at the end of file
    output = str(myanmarFloodedAreaDate.getInfo())+','+ str(myanmarFloodedHealthCenter.getInfo())+','+str(myanmarNonFloodedHealthCenter.getInfo())
    f.write(output)
  else:
    print('Already Calculated') 


## ======================== End Calculation ============================ */

## ======================== Calculate and Save number of Flooded Health Center for Thailand ============================ */

# Select Thailand
thailand = countries.filter(ee.Filter.eq("country_na", "Thailand"))
thailandHospital = ee.FeatureCollection("users/kamalhosen/servir-mekong/thailand_hospital")
#print(thailandHospital.size().getInfo())
# Clip flood layer to thailand 
floodedWaterThailand = floodedWater.clip(thailand)
selectThailandFloodedWaterPixel = floodedWaterThailand.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterThailand.get('system:time_start')).format('YYYY-MM-dd'))
#print(selectThailandFloodedWaterPixel.getInfo())

sampleHospitalThailand = floodedWaterThailand.unmask(0).sampleRegions(
    collection = thailandHospital,
    scale = 100,
    tileScale = 16,
    geometries = True
)  
#print(sampleHospital)
nonFloodedHospitalThailand = sampleHospitalThailand.filter(ee.Filter.eq("water",0))
floodedHospitalThailand = sampleHospitalThailand.filter(ee.Filter.gt("water",0))

thailandNonFloodedHealthCenter = ee.Number(nonFloodedHospitalThailand.size())
thailandFloodedHealthCenter = ee.Number(floodedHospitalThailand.size())
thailandFloodedAreaDate = ee.String(selectThailandFloodedWaterPixel.get('date'))
print(thailandNonFloodedHealthCenter.getInfo(), thailandFloodedHealthCenter.getInfo(), thailandFloodedAreaDate.getInfo())

# if os.path.exists('./static/data/thailand/thailand_flooded_health_center.txt') == False: 
#   series = "Date,thailandFloodedHealthCenter,thailandNonFloodedHealthCenter"
#   output = series +'\n'+str(thailandFloodedAreaDate.getInfo())+','+ str(thailandFloodedHealthCenter.getInfo())+','+str(thailandNonFloodedHealthCenter.getInfo())
#   print(output)
# else:
#   print ("Already calculated.")

with open('./static/data/thailand/thailand_flooded_health_center.txt', "a+") as f:
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
    f.write("\n")
    # Append text at the end of file
    output = str(thailandFloodedAreaDate.getInfo())+','+ str(thailandFloodedHealthCenter.getInfo())+','+str(thailandNonFloodedHealthCenter.getInfo())
    f.write(output)
  else:
    print('Already Calculated') 


## ======================== End Calculation ============================ */

## ======================== Calculate and Save number of Flooded Health Center for Vietnam ============================ */

# Select Vietnam
vietnam = countries.filter(ee.Filter.eq("country_na", "Vietnam"))
vietnamHospital = ee.FeatureCollection("users/kamalhosen/servir-mekong/vietnam_hospital")
#print(vietnamHospital.size().getInfo())
# Clip flood layer to vietnam 
floodedWaterVietnam = floodedWater.clip(vietnam)
selectVietnamFloodedWaterPixel = floodedWaterVietnam.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterVietnam.get('system:time_start')).format('YYYY-MM-dd'))
#print(selectVietnamFloodedWaterPixel.getInfo())

sampleHospitalVietnam = floodedWaterVietnam.unmask(0).sampleRegions(
    collection = vietnamHospital,
    scale = 100,
    tileScale = 16,
    geometries = True
)  
#print(sampleHospital)
nonFloodedHospitalVietnam = sampleHospitalVietnam.filter(ee.Filter.eq("water",0))
floodedHospitalVietnam = sampleHospitalVietnam.filter(ee.Filter.gt("water",0))

vietnamNonFloodedHealthCenter = ee.Number(nonFloodedHospitalVietnam.size())
vietnamFloodedHealthCenter = ee.Number(floodedHospitalVietnam.size())
vietnamFloodedAreaDate = ee.String(selectVietnamFloodedWaterPixel.get('date'))
print(vietnamNonFloodedHealthCenter.getInfo(), vietnamFloodedHealthCenter.getInfo(), vietnamFloodedAreaDate.getInfo())

# if os.path.exists('./static/data/vietnam/vietnam_flooded_health_center.txt') == False: 
#   series = "Date,vietnamFloodedHealthCenter,vietnamNonFloodedHealthCenter"
#   output = series +'\n'+str(vietnamFloodedAreaDate.getInfo())+','+ str(vietnamFloodedHealthCenter.getInfo())+','+str(vietnamNonFloodedHealthCenter.getInfo())
#   print(output)
# else:
#   print ("Already calculated.")

with open('./static/data/vietnam/vietnam_flooded_health_center.txt', "a+") as f:
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
    f.write("\n")
    # Append text at the end of file
    output = str(vietnamFloodedAreaDate.getInfo())+','+ str(vietnamFloodedHealthCenter.getInfo())+','+str(vietnamNonFloodedHealthCenter.getInfo())
    f.write(output)
  else:
    print('Already Calculated') 

## ======================== End Calculation ============================ */

## ======================== Calculate and Save number of Flooded Education Center for Cambodia ============================ */

# Select Cambodia Education
cambodiaEducation = ee.FeatureCollection("users/kamalhosen/servir-mekong/cambodia_education")
#print(cambodiaEducation.size().getInfo())

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
print(cambodiaNonFloodedEducationCenter.getInfo(), cambodiaFloodedEducationCenter.getInfo(), cambodiaFloodedAreaDate.getInfo())

# if os.path.exists('./static/data/cambodia/cambodia_flooded_education_center.txt') == False: 
#   series = "Date,cambodiaFloodedEducationCenter,cambodiaNonFloodedEducationCenter"
#   output = series +'\n'+str(cambodiaFloodedAreaDate.getInfo())+','+ str(cambodiaFloodedEducationCenter.getInfo())+','+str(cambodiaNonFloodedEducationCenter.getInfo())
#   print(output)
# else:
#   print ("Already calculated.")

with open('./static/data/cambodia/cambodia_flooded_education_center.txt', "a+") as f:
  f.seek(0)
  data = pd.read_csv(f)
  lastline = data.tail(1)
  date = lastline['Date'].values[0]

  if len(data) > 0 and date != recent_date:
    f.write("\n")
    output = str(cambodiaFloodedAreaDate.getInfo())+','+ str(cambodiaFloodedEducationCenter.getInfo())+','+str(cambodiaNonFloodedEducationCenter.getInfo())
    f.write(output)
  else:
    print('Already Calculated') 


## ======================== End Calculation ============================ */

## ======================== Calculate and Save number of Flooded Education Center for Laos ============================ */

# Select Laos Education
laosEducation = ee.FeatureCollection("users/kamalhosen/servir-mekong/laos_education")
#print(laosEducation.size().getInfo())

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
print(laosNonFloodedEducationCenter.getInfo(), laosFloodedEducationCenter.getInfo(), laosFloodedAreaDate.getInfo())

# if os.path.exists('./static/data/laos/laos_flooded_education_center.txt') == False: 
#   series = "Date,laosFloodedEducationCenter,laosNonFloodedEducationCenter"
#   output = series +'\n'+str(laosFloodedAreaDate.getInfo())+','+ str(laosFloodedEducationCenter.getInfo())+','+str(laosNonFloodedEducationCenter.getInfo())
#   print(output)
# else:
#   print ("Already calculated.")

with open('./static/data/laos/laos_flooded_education_center.txt', "a+") as f:
  f.seek(0)
  data = pd.read_csv(f)
  lastline = data.tail(1)
  date = lastline['Date'].values[0]

  if len(data) > 0 and date != recent_date:
    f.write("\n")
    output = str(laosFloodedAreaDate.getInfo())+','+ str(laosFloodedEducationCenter.getInfo())+','+str(laosNonFloodedEducationCenter.getInfo())
    f.write(output)
  else:
    print('Already Calculated') 


## ======================== End Calculation ============================ */


## ======================== Calculate and Save number of Flooded Education Center for Myanmar ============================ */

# Select Myanmar Education
myanmarEducation = ee.FeatureCollection("users/kamalhosen/servir-mekong/myanmar_education")
#print(myanmarEducation.size().getInfo())

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
print(myanmarNonFloodedEducationCenter.getInfo(), myanmarFloodedEducationCenter.getInfo(), myanmarFloodedAreaDate.getInfo())

# if os.path.exists('./static/data/myanmar/myanmar_flooded_education_center.txt') == False: 
#   series = "Date,myanmarFloodedEducationCenter,myanmarNonFloodedEducationCenter"
#   output = series +'\n'+str(myanmarFloodedAreaDate.getInfo())+','+ str(myanmarFloodedEducationCenter.getInfo())+','+str(myanmarNonFloodedEducationCenter.getInfo())
#   print(output)
# else:
#   print ("Already calculated.")

with open('./static/data/myanmar/myanmar_flooded_education_center.txt', "a+") as f:
  f.seek(0)
  data = pd.read_csv(f)
  lastline = data.tail(1)
  date = lastline['Date'].values[0]

  if len(data) > 0 and date != recent_date:
    f.write("\n")
    output = str(myanmarFloodedAreaDate.getInfo())+','+ str(myanmarFloodedEducationCenter.getInfo())+','+str(myanmarNonFloodedEducationCenter.getInfo())
    f.write(output)
  else:
    print('Already Calculated') 

## ======================== End Calculation ============================ */

## ======================== Calculate and Save number of Flooded Education Center for Thailand ============================ */

# Select Thailand Education
thailandEducation = ee.FeatureCollection("users/kamalhosen/servir-mekong/thailand_education")
#print(thailandEducation.size().getInfo())

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
print(thailandNonFloodedEducationCenter.getInfo(), thailandFloodedEducationCenter.getInfo(), thailandFloodedAreaDate.getInfo())

# if os.path.exists('./static/data/thailand/thailand_flooded_education_center.txt') == False: 
#   series = "Date,thailandFloodedEducationCenter,thailandNonFloodedEducationCenter"
#   output = series +'\n'+str(thailandFloodedAreaDate.getInfo())+','+ str(thailandFloodedEducationCenter.getInfo())+','+str(thailandNonFloodedEducationCenter.getInfo())
#   print(output)
# else:
#   print ("Already calculated.")

with open('./static/data/thailand/thailand_flooded_education_center.txt', "a+") as f:
  f.seek(0)
  data = pd.read_csv(f)
  lastline = data.tail(1)
  date = lastline['Date'].values[0]

  if len(data) > 0 and date != recent_date:
    f.write("\n")
    output = str(thailandFloodedAreaDate.getInfo())+','+ str(thailandFloodedEducationCenter.getInfo())+','+str(thailandNonFloodedEducationCenter.getInfo())
    f.write(output)
  else:
    print('Already Calculated') 


## ======================== End Calculation ============================ */

## ======================== Calculate and Save number of Flooded Education Center for Vietnam ============================ */

# Select Vietnam Education
vietnamEducation = ee.FeatureCollection("users/kamalhosen/servir-mekong/vietnam_education")
#print(vietnamEducation.size().getInfo())

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
print(vietnamNonFloodedEducationCenter.getInfo(), vietnamFloodedEducationCenter.getInfo(), vietnamFloodedAreaDate.getInfo())

# if os.path.exists('./static/data/vietnam/vietnam_flooded_education_center.txt') == False: 
#   series = "Date,vietnamFloodedEducationCenter,vietnamNonFloodedEducationCenter"
#   output = series +'\n'+str(vietnamFloodedAreaDate.getInfo())+','+ str(vietnamFloodedEducationCenter.getInfo())+','+str(vietnamNonFloodedEducationCenter.getInfo())
#   print(output)
# else:
#   print ("Already calculated.")

with open('./static/data/vietnam/vietnam_flooded_education_center.txt', "a+") as f:
  f.seek(0)
  data = pd.read_csv(f)
  lastline = data.tail(1)
  date = lastline['Date'].values[0]

  if len(data) > 0 and date != recent_date:
    f.write("\n")
    output = str(vietnamFloodedAreaDate.getInfo())+','+ str(vietnamFloodedEducationCenter.getInfo())+','+str(vietnamNonFloodedEducationCenter.getInfo())
    f.write(output)
  else:
    print('Already Calculated') 

## ======================== End Calculation ============================ */
