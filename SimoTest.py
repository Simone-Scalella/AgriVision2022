import fiona
import rasterio
import rasterio.mask
import shapely.geometry
from matplotlib import pyplot as plt

'''f= rasterio.open(r'OUTPUT.tif')
campo = rasterio.open(r'content2\data\2016-11-15.tiff')
print(f.shape)
print(campo.shape)'''


from rasterio.features import shapes
mask = None
with rasterio.Env():
    with rasterio.open(r'content2\data\2016-11-15.tiff',"r") as src:
        image = src.read(1) # first band
        results = (
        {'properties': {'raster_val': v}, 'geometry': s}
        for i, (s, v) 
        in enumerate(
            shapes(image, mask=mask, transform=src.transform)))
geoms = list(results)
 # first feature
print(geoms[0])

from shapely.geometry import shape
print(shape(geoms[0]['geometry']))
print(type(shape(geoms[0]['geometry'])))



out_image, out_transform = rasterio.mask.mask(rasterio.open(r'content2\data\2016-11-15.tiff','r'), [shape(geoms[0]['geometry'])], crop=True)
out_meta = rasterio.open(r'content2\data\2016-11-15.tiff','r').meta

print(type(out_image))
plt.plot(out_image[0])
plt.show()