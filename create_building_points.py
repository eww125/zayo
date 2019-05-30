import pandas as pd
#import geopandas
import matplotlib.pyplot as plt
from shapely.geometry import Point
from geopandas import GeoDataFrame
#pd.set_option('display.expand_frame_repr', False)

df = pd.read_excel('On-Net-Building-List-External-ver.03152019.xlsx', skiprows=1)
df.columns = df.columns.str.replace(' ', '_')
df.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)

geometry = [Point(xy) for xy in zip(df.LONGITUDE, df.LATITUDE)]
crs = {'init': 'epsg:4326'}
gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
#print(gdf.head())

#gdf.to_file("buildings.shp")

df.rename(columns={'STRUCTURE_CATEGOGY':'STRUCTURE_CATEGORY'}, inplace=True)
##print(df.groupby(['STRUCTURE_CATEGORY']).size().reset_index(name='count'))


df['LAT_LON'] = df['LATITUDE'].map(str) + df['LONGITUDE'].map(str)
#print(df.head())

duplicate_locations = pd.concat(g for _, g in df.groupby("LAT_LON") if len(g) > 1)
print(len(duplicate_locations))
duplicate_locations.to_csv('duplicate_locations.csv')