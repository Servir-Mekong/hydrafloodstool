from datetime import date
import ee, os, csv
ee.Initialize()

with open('./static/data/' + str('cambodia3') + '.txt', 'w') as txt:
  series = "Date, TotalAreainSqKm"
  txt.write(series)
  txt.close()

def getDateList():
    pickup_dict = {}
    def imgDate(d):
      return ee.Date(d).format("YYYY-MM-dd")
    ImageCollection = ee.ImageCollection("projects/servir-mekong/hydrafloodsS1Daily")
    dates = ee.List(ImageCollection.aggregate_array("system:time_start")).map(imgDate).getInfo()
    return dates
dateList = getDateList()

# Datewise Calculations
for i in dateList: 
  # SERVIR-Mekong sentinel 1 surface water 
  sw = ee.ImageCollection("projects/servir-mekong/hydrafloodsS1Daily")

  # Import country layers
  countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
  # Select Cambodia
  cambodia = countries.filter(ee.Filter.eq("country_na", "Cambodia"))

  # Filter collection
  fc = sw.filterDate(i)
  filtered_sw = ee.Image(fc.first()).select(0)

  # JRC Image Collection version GSW1_3
  waterOcc = ee.Image('JRC/GSW1_3/GlobalSurfaceWater').select('occurrence')
  jrc_data0 = ee.Image("JRC/GSW1_3/Metadata").select('total_obs').lte(0)
  waterOccFilled = waterOcc.unmask(0).max(jrc_data0)
  waterMask = waterOccFilled.lt(50)

  # Mask surface water layer by JRC permanent water layer
  floodedWater = filtered_sw.updateMask(waterMask)

  # Clip flood layer to cambodia 
  floodedWaterCambodia = floodedWater.clip(cambodia)

  selectCambodiaFloodedWaterPixel = floodedWaterCambodia.select(0).multiply(ee.Image.pixelArea())

  khFloodedAreas = selectCambodiaFloodedWaterPixel.reduceRegion(
      reducer = ee.Reducer.sum(),
      geometry = cambodia.geometry(),
      scale = 10,
      maxPixels = 1e13
  )
  #print(khFloodedAreas.getInfo())
  khFloodedAreaSqKm = ee.Number(khFloodedAreas.get('water')).divide(1e6).round()
  khFloodedAreaDate = ee.String(ee.Date(floodedWaterCambodia.get('system:time_start')).format('YYYY-MM-dd'))
  print(khFloodedAreaSqKm.getInfo(), khFloodedAreaDate.getInfo())

  with open('./static/data/' + str('cambodia3') + '.txt', "a+") as file_object:
    # Move read cursor to the start of file.
    file_object.seek(0)
    # If file is not empty then append '\n'
    data = file_object.read(100)
    if len(data) > 0 :
        file_object.write("\n")
    # Append text at the end of file
    output = str(khFloodedAreaDate.getInfo())+','+ str(khFloodedAreaSqKm.getInfo())
    file_object.write(output)

# -*- coding: utf-8 -*-
from datetime import date
from unittest import result
import ee, os, csv
ee.Initialize()

# SERVIR-Mekong sentinel 1 surface water 
sw = ee.ImageCollection("projects/servir-mekong/hydrafloodsS1Daily")

# Import country layers
countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
# Select Cambodia
cambodia = countries.filter(ee.Filter.eq("country_na", "Cambodia"))

## ======================== For single image ============================ */
# Filter collection
fc = sw.filterDate('2021-01-30')
filtered_sw = ee.Image(fc.first()).select(0)

# JRC Image Collection version GSW1_3
waterOcc = ee.Image('JRC/GSW1_3/GlobalSurfaceWater').select('occurrence')
jrc_data0 = ee.Image("JRC/GSW1_3/Metadata").select('total_obs').lte(0)
waterOccFilled = waterOcc.unmask(0).max(jrc_data0)
waterMask = waterOccFilled.lt(50)

# Mask surface water layer by JRC permanent water layer
floodedWater = filtered_sw.updateMask(waterMask)

# Clip flood layer to cambodia 
floodedWaterCambodia = floodedWater.clip(cambodia)
selectCambodiaFloodedWaterPixel = floodedWaterCambodia.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterCambodia.get('system:time_start')).format('YYYY-MM-dd'))
#print(selectCambodiaFloodedWaterPixel.getInfo())

khFloodedAreas = selectCambodiaFloodedWaterPixel.reduceRegion(
    reducer = ee.Reducer.sum(),
    geometry = cambodia.geometry(),
    scale = 10,
    maxPixels = 1e13
)
#print(khFloodedAreas.getInfo())
khFloodedAreaSqKm = ee.Number(khFloodedAreas.get('water')).divide(1e6).round()
khFloodedAreaDate = ee.String(selectCambodiaFloodedWaterPixel.get('date'))
print(khFloodedAreaSqKm.getInfo())
print(khFloodedAreaDate.getInfo())

if os.path.exists('./static/data/' + str('cambodia') + '.txt') == False: 
  series = "Date, TotalAreainSqKm"
  output = series +'\n'+str(khFloodedAreaDate.getInfo())+','+ str(khFloodedAreaSqKm.getInfo())
  print(output)
else:
  print ("Already calculated.")

with open('./static/data/' + str('cambodia') + '.txt', 'w') as txt:
  series = "Date, TotalAreainSqKm"
  output = series +'\n'+str(khFloodedAreaDate.getInfo())+','+ str(khFloodedAreaSqKm.getInfo())
  txt.write(output)


# ## /* ==================== For Every Image in a Image Collection =================== */
# # Filtered collection
# filteredCollection = sw.filterDate('2022-01-01', '2022-01-03')

# # Define function to mask surface water by permamanet water 
# def permanentWaterMask(img):
#   waterOcc = ee.Image('JRC/GSW1_3/GlobalSurfaceWater').select('occurrence')
#   jrc_data0 = ee.Image("JRC/GSW1_3/Metadata").select('total_obs').lte(0)
#   waterOccFilled = waterOcc.unmask(0).max(jrc_data0)
#   waterMask = waterOccFilled.lt(50)
#   return img.updateMask(waterMask)

# # Seperate flooded water from permanent water
# onlyFloodedWater = sw.map(permanentWaterMask)

# # Define function to clip flooded water by country Cambodia
# def clipByCambodia(img):
#     return img.clip(cambodia)

# cambodiaFloodedWater = onlyFloodedWater.map(clipByCambodia)
# #print(cambodiaFloodedWater.getInfo())

# # Select only water pixel
# selectCambodiaFloodedWaterPixel = cambodiaFloodedWater.select(0)
# # Define function to calculate total flooded area for cambodia
# def calcFloodedArea(img):
#   area = img.reduceRegion(
#     reducer = ee.Reducer.sum(),
#     geometry = cambodia.geometry(),
#     scale = 10,
#     maxPixels = 1e13
#   )
#   areaSqKM = ee.Number(area.get('water')).divide(1e6).round()
#   return img.set('FloodedArea', areaSqKM).set('Date', ee.Date(img.get('system:time_start')).format('YYYY-MM-dd'))

# cambodiaFloodedArea = selectCambodiaFloodedWaterPixel.map(calcFloodedArea)
# print(cambodiaFloodedArea.getInfo())

# # cambodiaFloodedAreaSqKm = ee.Number(cambodiaFloodedArea.get('FloodedArea'))
# # cambodiaAreaDate = ee.String(cambodiaFloodedArea.get('Date'))

# def getDateList():       
#   ImageCollection = ee.ImageCollection(cambodiaFloodedArea)
#   dates = ee.List(ImageCollection.aggregate_array("date")).getInfo()
#   return dates
# d = getDateList()
# print(d)

# def getAreaList():       
#   ImageCollection = ee.ImageCollection(cambodiaFloodedArea)
#   FloodAreas = ee.List(ImageCollection.aggregate_array("FloodedArea")).getInfo()
#   return FloodAreas
# a = getAreaList()
# print(a)

# ll = [d, a]
# # if os.path.exists('./static/data/' + str('cambodia2') + '.txt') == False: 
# #   series = "Date, TotalAreainSqKm"
# #   output = series +'\n'+str(cambodiaAreaDate.getInfo())+','+ str(cambodiaFloodedAreaSqKm.getInfo())
# #   print(output)
# # else:
# #   print ("Already calculated.")

# # with open('./static/data/' + str('cambodia2') + '.txt', 'w') as txt:
# #   series = "Date, TotalAreainSqKm"
# #   output = series +'\n'+str(cambodiaAreaDate.getInfo())+','+ str(cambodiaFloodedAreaSqKm.getInfo())
# #   txt.write(output)


# # SERVIR-Mekong sentinel 1 surface water 
# sw = ee.ImageCollection("projects/servir-mekong/hydrafloodsS1Daily")

# # Import country layers
# countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")

# # Filter collection
# fc = sw.filterDate(recent_date)
# filtered_sw = ee.Image(fc.first()).select(0)

# # JRC Image Collection version GSW1_3
# waterOcc = ee.Image('JRC/GSW1_3/GlobalSurfaceWater').select('occurrence')
# jrc_data0 = ee.Image("JRC/GSW1_3/Metadata").select('total_obs').lte(0)
# waterOccFilled = waterOcc.unmask(0).max(jrc_data0)
# waterMask = waterOccFilled.lt(50)

# # Mask surface water layer by JRC permanent water layer
# floodedWater = filtered_sw.updateMask(waterMask)

# ## ======================== Calculate and Save Flooded Water Area for Thailand ============================ */

# # Select Thailand
# thailand = countries.filter(ee.Filter.eq("country_na", "Thailand"))

# # Clip flood layer to thailand 
# floodedWaterThailand = floodedWater.clip(thailand)
# selectThailandFloodedWaterPixel = floodedWaterThailand.select(0).multiply(ee.Image.pixelArea()).set('date', ee.Date(floodedWaterThailand.get('system:time_start')).format('YYYY-MM-dd'))
# #print(selectThailandFloodedWaterPixel.getInfo())

# thailandFloodedArea = selectThailandFloodedWaterPixel.reduceRegion(
#   reducer = ee.Reducer.sum(),
#   geometry = thailand.geometry(),
#   scale = 30,
#   maxPixels = 1e13
# )
# #print(khFloodedAreas.getInfo())
# thailandFloodedAreaSqKm = ee.Number(thailandFloodedArea.get('water')).divide(1e6).round()
# thailandFloodedAreaDate = ee.String(selectThailandFloodedWaterPixel.get('date'))
# print(thailandFloodedAreaSqKm.getInfo(), thailandFloodedAreaDate.getInfo())

# if os.path.exists('./static/data/thailand/thailand_flooded_area.txt') == False: 
#   series = "Date,TotalAreainSqKm"
#   output = series +'\n'+str(thailandFloodedAreaDate.getInfo())+','+ str(thailandFloodedAreaSqKm.getInfo())
#   print(output)
# else:
#   print ("Already calculated.")
