import folium
import pandas as pd

#store info into variable df=data frame
df = pd.read_csv('volcano.txt')

#take the average values to adjust the center point on the map
latmean = df['LAT'].mean()
lonmean = df['LON'].mean()

map=folium.Map(location=[latmean, lonmean], zoom_start=6, tiles='Stamen Terrain')

#function to define color
def color(elev):
    if elev in range(0,1000):
        col= 'green'
    elif elev in range(1001,1999):
        col = 'blue'
    elif elev in range(2000,2999):
        col= 'orange'
    else:
        col= 'red'
    return col


#loop to create markers
#put 4 iterators into zip function
#read as iterator and then where there is a df to "grab" that iterator values

for lat,lon,name,elev in zip(df['LAT'], df['LON'], df['NAME'], df['ELEV']):
    folium.Marker(location=[lat, lon], popup = name, icon = folium.Icon(color=color(elev), icon_color='yellow', icon='cloud')).add_to(map)

print(map.save('volcano_final.html'))