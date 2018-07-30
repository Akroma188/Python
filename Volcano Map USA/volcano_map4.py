import folium
import pandas as pd

map4=folium.Map(location=[40.897934, -73.885948], zoom_start=5, tiles='Stamen Terrain')

folium.Marker(location=[40.897934, -73.885948], popup="I am so lost", icon = folium.Icon(icon = 'cloud')).add_to(map4)
folium.Marker(location=[40.8895439, -73.9015249], popup="But I can see you", icon = folium.Icon(color = 'green')).add_to(map4)

#store info into variable df=data frame
df = pd.read_csv('volcano.txt')

#create loop to create markers
#put 4 iterators into zip function
#read as iterator and then where there is a df to "grab" that iterator values

for lat,lon,name,elev in zip(df['LAT'], df['LON'], df['NAME'], df['ELEV']):
    folium.Marker(location=[lat, lon], popup = name, icon = folium.Icon(color='green' if elev in range(0, 1000) else 'orange' if elev in range(1001,1999) else 'blue' if elev in range(2000,2999) else 'red', icon='cloud')).add_to(map4)

print(map4.save('test5.html'))