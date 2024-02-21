import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import geemap.foliumap as geemap
import ee
ee.Initialize()

st.text('Draw polygon on map')
map=geemap.Map(center=[26,87],zoom=8)
map.to_streamlit()
if st.button('get_cooerd'):
   # data=map.user_roi
    #st.text(data)
    data=st_folium(map)
    print(data)




if st.button('show data'):
    st.write('retrieving data . . .')
    roi=map.draw_last_feature.geometry()

    
    
    
    
    moisture_collection=ee.ImageCollection("NASA/FLDAS/NOAH01/C/GL/M/V001")
    moisture_viz = {
    'min': 0.0,
    'max': 0.00005,
    'palette': ['black', 'blue', 'purple', 'cyan', 'green','yellow','red']
} 

    filtered_moisture=moisture_collection.filter(ee.Filter.date('2017-04-01', '2017-04-30')).filter(ee.Filter.bounds(roi)).select('SoilMoi00_10cm_tavg').first()
    reduced_moisture= filtered_moisture.reduceRegion(
    
    reducer=ee.Reducer.median(),
    geometry=roi,
    scale=10,
    maxPixels=1e10
      # Replace with the appropriate scale value
).getInfo()
    moisture=reduced_moisture['SoilMoi00_10cm_tavg']
    map.addLayer(filtered_moisture,moisture_viz, 'moisture Collection')
#soil_temperature
    roi=map.draw_last_feature.geometry()
    collection=ee.ImageCollection("NASA/FLDAS/NOAH01/C/GL/M/V001")
    temperature_viz = {
    'min': 0.0,
    'max': 0.00005,
    'palette': ['black', 'blue', 'purple', 'cyan', 'green','yellow','red']
}

    filtered_soil_temperature=collection.filter(ee.Filter.date('2017-04-01', '2017-04-30')).filter(ee.Filter.bounds(roi)).select('SoilTemp00_10cm_tavg').first()
    reduced_soil_temperature= filtered_soil_temperature.reduceRegion(
    
    reducer=ee.Reducer.median(),
    geometry=roi,
    scale=10,
    maxPixels=1e10
      # Replace with the appropriate scale value
).getInfo()
    soil_temperature=reduced_soil_temperature['SoilTemp00_10cm_tavg']
    map.addLayer(filtered_soil_temperature,temperature_viz, 'moisture Collection')
    data={'soil_moisture':moisture,'soil_temperature':soil_temperature
    
}
    df=pd.DataFrame(data,index=[0])
    st.write(df)
