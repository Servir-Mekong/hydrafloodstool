from datetime import date
from email import header
import ee, os, csv
ee.Initialize()

with open('./static/data/laos_flooded_area.txt', 'w') as txt:
  header = "Date,TotalAreainSqKm"
  txt.write(header)
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

  # Select Laos
  laos = countries.filter(ee.Filter.eq("country_na", "Laos"))

  # Clip flood layer to laos 
  floodedWaterLaos = floodedWater.clip(laos)

  selectLaosFloodedWaterPixel = floodedWaterLaos.select(0).multiply(ee.Image.pixelArea())

  laosFloodedArea = selectLaosFloodedWaterPixel.reduceRegion(
      reducer = ee.Reducer.sum(),
      geometry = laos.geometry(),
      scale = 10,
      maxPixels = 1e13
  )
  #print(khFloodedAreas.getInfo())
  laosFloodedAreaSqKm = ee.Number(laosFloodedArea.get('water')).divide(1e6).round()
  laosFloodedAreaDate = ee.String(ee.Date(floodedWaterLaos.get('system:time_start')).format('YYYY-MM-dd'))
  print(laosFloodedAreaSqKm.getInfo(), laosFloodedAreaDate.getInfo())

  with open('./static/data/laos_flooded_area.txt', 'a+') as f:
    # Move read cursor to the start of file.
    f.seek(0)
    # If file is not empty then append '\n'
    data = f.read(100)
    if len(data) > 0 :
        f.write("\n")
    # Append text at the end of file
    output = str(laosFloodedAreaDate.getInfo())+','+ str(laosFloodedAreaSqKm.getInfo())
    f.write(output)