import folium

m = folium.Map(location=[30.3088, -89.3300], zoom_start=13)

folium.Marker(
    location=[30.32, -89.3300],
    popup="A Place Apart",
    icon=folium.Icon(color="green"),
).add_to(m)

m.save("map.html")