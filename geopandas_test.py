import geopandas as gpd
from shapely.geometry import Point, LinearRing, Polygon

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

hsv_df = gpd.read_file('./map.geojson')

hsv_poly = gpd.GeoDataFrame(geometry=[i for i in hsv_df['geometry'] if(type(i) == Polygon)])
hsv_markers = gpd.GeoDataFrame(geometry=[i for i in hsv_df['geometry'] if(type(i) == Point)])

# Need a relation of each point to each PolyGon
for i in hsv_poly['geometry']:
    print("Poly: {}, Area: {}".format(i, i.area))
    for j in hsv_markers['geometry']:
        if(j.within(i)):
            print("Point ({}, {}) is within the Polygon.".format(j.x, j.y))
        else:
            # Need to finish by using this reference: https://gis.stackexchange.com/questions/279109/calculate-distance-between-a-coordinate-and-a-county-in-geopandas
            # Also using: https://automating-gis-processes.github.io/site/notebooks/L2/calculating-distances.html
            dist = i.distance(j)
            print("The Point is {} units from the Polygon.".format(dist))
            