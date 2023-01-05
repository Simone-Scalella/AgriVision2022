import fiona
from shapely.geometry import mapping, Polygon

shp = fiona.open(r"yield\2017 Mappa resa Grano Duro NH Valle sq4.shp", "r")
shp2 = fiona.open(r"yield\2017 Mappa resa Grano Duro NH Valle sq4 - parte2.shp", "r")
shapes = [feature["geometry"] for feature in shp]
shapes2 = [feature["geometry"] for feature in shp2]
'''for item in shapes:
    print(item['coordinates'])'''
union = shapes.append(shapes2)
poly = Polygon([[p['coordinates'][0], p['coordinates'][1]] for p in shapes])
print(poly)

# Define a polygon feature geometry with one attribute
schema = {
    'geometry': 'Polygon',
    'properties': {'id': 'int'},
}

# Write a new Shapefile
with fiona.open('my_shp2.shp', 'w', 'ESRI Shapefile', schema) as c:
    ## If there are multiple geometries, put the "for" loop here
    c.write({
        'geometry': mapping(poly),
        'properties': {'id': 123},
    })