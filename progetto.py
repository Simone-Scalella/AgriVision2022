# load and display an image with Matplotlib
import matplotlib.pyplot as plt

import numpy as np
from osgeo import gdal

from sentinelhub import SHConfig
from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, \
    DataCollection, bbox_to_dimensions, DownloadRequest

config = SHConfig()

config.sh_client_id = '***REMOVED***'
config.sh_client_secret = 'x^X%K7Yn@w<)Jl?177A/](~4Te96x#vpzKun8xCE'
config.save()

evalscript = """
    //VERSION=3
function setup() {
  return {
    input: [{
      bands: ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B11", "B12"],
      units: "DN"
    }],
    output: {
      id: "default",
      bands: 12,
      sampleType: SampleType.UINT16
    }
  }
}
function evaluatePixel(sample) {
    return [ sample.B01, sample.B02, sample.B03, sample.B04, sample.B05, sample.B06, sample.B07, sample.B08, sample.B8A, sample.B09, sample.B11, sample.B12]
}
"""
filelist = ['2016-11-12', '2016-11-15', '2016-11-22', '2016-11-25', '2016-11-05', '2016-12-12', '2016-12-15', '2016-12-02', '2016-12-22', '2016-12-25', '2016-12-05', '2017-01-01', '2017-01-14', '2017-01-24', '2017-01-31', '2017-01-04', '2017-02-10', '2017-02-13', '2017-02-20', '2017-02-23', '2017-02-03', '2017-03-12', '2017-03-15', '2017-03-02', '2017-03-22', '2017-03-25', '2017-03-25', '2017-03-05', '2017-04-01', '2017-04-11', '2017-04-11', '2017-04-14', '2017-04-21', '2017-04-24', '2017-04-04', '2017-05-01', '2017-05-11', '2017-05-14', '2017-05-21', '2017-05-24', '2017-05-31', '2017-05-04', '2017-06-10', '2017-06-13', '2017-06-20', '2017-06-23', '2017-06-03', '2017-06-30', '2017-07-10', '2017-07-13', '2017-07-15', '2017-07-18', '2017-07-20', '2017-07-23', '2017-07-25', '2017-07-28', '2017-07-03', '2017-07-30', '2017-07-08']

request_raw_list_dict = []
for i in range(len(filelist)):
  start = filelist[i]+"T00:00:00Z"
  stop = filelist[i]+"T23:59:59Z"
  request_raw_dict = {
      "input": {
          "bounds": {
              "properties": {
                  "crs": "http://www.opengis.net/def/crs/EPSG/0/32633"
              },
              "geometry": {
                  "type": "Polygon",
                  "coordinates": 
          [ [ [ 275313.225371220265515, 4930657.958802883513272 ], [ 275388.914355162938591, 4932845.371425414457917 ], [ 278329.683593424211722, 4932744.26427542604506 ], [ 278254.987197705253493, 4930556.852888375520706 ], [ 275313.225371220265515, 4930657.958802883513272 ] ] ]
              }
          },
          "data": [
              {
                  "type": "S2L2A",
                  "dataFilter": {
                      "timeRange": {
                          "from": start,
                          "to": stop
                      }
                  },"processing": {
            "upsampling": "NEAREST",
            "downsampling": "NEAREST"
            }
              }
          ]
      },
      "output": {
          "resx": 10,
          "resy": 10,
          "responses": [
              {
                  "identifier": "default",
                  "format": {
                      'type': "image/tiff"
                  }
              }
          ]
      },
      "evalscript": evalscript
  }
  request_raw_list_dict.append(request_raw_dict)

import time
import os

for i in range(31,len(request_raw_list_dict)):
#for i in range(2):
  # create request
  print(filelist[i] + ".tiff")
  download_request = DownloadRequest(
      request_type='POST',
      url="https://services.sentinel-hub.com/api/v1/process",
      post_values=request_raw_list_dict[i],
      data_type=MimeType.TIFF,
      headers={'content-type': 'application/json'},
      use_session=True,
      save_response = True,
      data_folder = "./content/data",
      filename = filelist[i] + ".tiff"
  )  
  # execute request
  #print(img[100:102,100:102,0])
  client = SentinelHubDownloadClient(config=config)
  img = client.download(download_request)
  print(os.path.getsize("./content/data/" + filelist[i] + ".tiff"))  
  #time.sleep(45)

tiff_file = "./ravenna/bands/content/data/2016-11-15.tiff"
dataset = gdal.Open(tiff_file)
band1 = dataset.GetRasterBand(1).ReadAsArray()
band2 = dataset.GetRasterBand(2).ReadAsArray()
band3 = dataset.GetRasterBand(3).ReadAsArray()

#plt.figure()

f, axarr = plt.subplots(1,3) 
axarr[0].imshow(band1)
axarr[1].imshow(band2)
axarr[2].imshow(band3)
plt.show()

#geo_tiff = GeoTiff(tiff_file)
#array = np.array(geo_tiff.read())
#print(array)
#image.imshow(array)
#image = image.imread("./ravenna/bands/content/data/2016-11-15.tiff")
#img = georaster.MultiBandRaster('./ravenna/bands/content/data/2016-11-15.tiff')
#pyplot.imshow(img.r[:,:,2])
#pyplot.show()