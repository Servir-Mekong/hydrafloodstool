from datetime import date
from genericpath import exists
from unittest import result
import ee, os, csv
import pandas as pd
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

with open('/home/ubuntu/hydrafloodstool/hydrafloodviewer/static/data/cambodia/cambodia_flooded_districts.txt', "a+") as f:
  # Move read cursor to the start of file.
  f.seek(0)
  if f.read() == "" :
    header = "Date,NumberOfFloodedDistricts"
    f.write(header)
    f.close()
  else:
    print("Header Exist")

with open('/home/ubuntu/hydrafloodstool/hydrafloodviewer/static/data/cambodia/cambodia_flooded_districts.txt', "a+") as f:
  # Move read cursor to the start of file.
  f.seek(0)
  data = pd.read_csv(f)

  if len(data) <= 0:

    # SERVIR-Mekong sentinel 1 surface water 
    sw = ee.ImageCollection("projects/servir-mekong/hydrafloodsS1Daily")

    # Import country layers
    countries = ee.FeatureCollection("FAO/GAUL/2015/level2")

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
    cambodia = countries.filter(ee.Filter.eq("ADM0_NAME", "Cambodia"))

    # Clip flood layer to cambodia 
    floodedWaterCambodia = floodedWater.clip(cambodia)
    selectCambodiaFloodedWaterPixel = floodedWaterCambodia.multiply(ee.Image.pixelArea()).divide(1e6).set('date', ee.Date(floodedWaterCambodia.get('system:time_start')).format('YYYY-MM-dd'))
    #print(selectCambodiaFloodedWaterPixel.getInfo())

    DISTRICT_FLOOD_THRESHOLD = 10

    def calcArea(feature):
      fldArea = selectCambodiaFloodedWaterPixel.unmask(0).reduceRegion(
        reducer = ee.Reducer.sum(),
        geometry = feature.geometry(),
        # scale: 100,
        maxPixels = 1e13
      )
      district = feature.get('ADM2_NAME')
      return ee.Feature(
        feature.geometry(),
        fldArea.set('district', district).set('water_frac', ee.Number(fldArea.get('water')).divide(feature.geometry().area().divide(1e6)))
      )

    districtArea = cambodia.map(calcArea)
    #print(districtArea)
    cambodiaFloodedDistricts = districtArea.filter(ee.Filter.gt("water",DISTRICT_FLOOD_THRESHOLD))
    # print('Number of Flooded Districts:', floodedDistricts.size().getInfo())
    cambodiaFloodedAreaDate = ee.String(selectCambodiaFloodedWaterPixel.get('date'))
    print(cambodiaFloodedAreaDate.getInfo(), cambodiaFloodedDistricts.size().getInfo())

    f.write("\n")
    # Append text at the end of file
    output = str(cambodiaFloodedAreaDate.getInfo())+','+ str(cambodiaFloodedDistricts.size().getInfo())
    f.write(output)
  else: 
    # Get last row 
    lastline = data.tail(1)
    # Get date
    date = lastline['Date'].values[0]
    # print(date)

    if date != recent_date:
      # SERVIR-Mekong sentinel 1 surface water 
      sw = ee.ImageCollection("projects/servir-mekong/hydrafloodsS1Daily")

      # Import country layers
      countries = ee.FeatureCollection("FAO/GAUL/2015/level2")

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
      cambodia = countries.filter(ee.Filter.eq("ADM0_NAME", "Cambodia"))

      # Clip flood layer to cambodia 
      floodedWaterCambodia = floodedWater.clip(cambodia)
      selectCambodiaFloodedWaterPixel = floodedWaterCambodia.multiply(ee.Image.pixelArea()).divide(1e6).set('date', ee.Date(floodedWaterCambodia.get('system:time_start')).format('YYYY-MM-dd'))
      #print(selectCambodiaFloodedWaterPixel.getInfo())

      DISTRICT_FLOOD_THRESHOLD = 10

      def calcArea(feature):
        fldArea = selectCambodiaFloodedWaterPixel.unmask(0).reduceRegion(
          reducer = ee.Reducer.sum(),
          geometry = feature.geometry(),
          # scale: 100,
          maxPixels = 1e13
        )
        district = feature.get('ADM2_NAME')
        return ee.Feature(
          feature.geometry(),
          fldArea.set('district', district).set('water_frac', ee.Number(fldArea.get('water')).divide(feature.geometry().area().divide(1e6)))
        )

      districtArea = cambodia.map(calcArea)
      #print(districtArea)
      cambodiaFloodedDistricts = districtArea.filter(ee.Filter.gt("water",DISTRICT_FLOOD_THRESHOLD))
      # print('Number of Flooded Districts:', floodedDistricts.size().getInfo())
      cambodiaFloodedAreaDate = ee.String(selectCambodiaFloodedWaterPixel.get('date'))
      print(cambodiaFloodedAreaDate.getInfo(), cambodiaFloodedDistricts.size().getInfo())

      f.write("\n")
      # Append text at the end of file
      output = str(cambodiaFloodedAreaDate.getInfo())+','+ str(cambodiaFloodedDistricts.size().getInfo())
      f.write(output)
    else: 
      print('Already Calculated')

  ## ======================== End Calculation ============================ */