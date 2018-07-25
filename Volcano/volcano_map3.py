import folium
import pandas as pd

map3=folium.Map(location=[40.897934, -73.885948], zoom_start=5, tiles='Stamen Terrain')

folium.Marker(location=[40.897934, -73.885948], popup="I am so lost", icon = folium.Icon(icon = 'cloud')).add_to(map3)
folium.Marker(location=[40.8895439, -73.9015249], popup="But I can see you", icon = folium.Icon(color = 'green')).add_to(map3)

#store info into variable df=data frame
df = pd.read_csv('volcano.txt')

#create loop to create markers
#put 3 iterators into zip function
#read as iterator and then where there is a df to "grab" that iterator values

for lat,lon,name in zip(df['LAT'], df['LON'], df['NAME']):
    folium.Marker(location=[lat, lon], popup = name, icon = folium.Icon(icon='cloud')).add_to(map3)

print(map3.save('test4.html'))
