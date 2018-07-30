import folium

#First Map
map=folium.Map(location=[40.897934, -73.885948], zoom_start=7) 
print(map.save('test.html'))
#Secon Map
map2= folium.Map(location=[40.897934, -73.885948], zoom_start=15, tiles='Stamen Terrain')
print(map2.save('test2.html'))