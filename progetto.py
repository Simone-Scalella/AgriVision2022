# load and display an image with Matplotlib
import matplotlib.pyplot as plt

import numpy as np
from osgeo import gdal



tiff_file = "./ravenna/bands/content/data/2016-11-15.tiff"
dataset = gdal.Open(tiff_file)
band = dataset.GetRasterBand(1)
arr = band.ReadAsArray()
print(arr)
plt.imshow(arr)
plt.show()

#geo_tiff = GeoTiff(tiff_file)
#array = np.array(geo_tiff.read())
#print(array)
#image.imshow(array)
#image = image.imread("./ravenna/bands/content/data/2016-11-15.tiff")
#img = georaster.MultiBandRaster('./ravenna/bands/content/data/2016-11-15.tiff')
#pyplot.imshow(img.r[:,:,2])
#pyplot.show()