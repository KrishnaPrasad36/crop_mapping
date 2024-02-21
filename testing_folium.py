import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import geemap.foliumap as geemap
import ee
from folium.plugins import Draw
import requests
import pandas as pd
ee.Initialize()
st.text('Draw polygon on map')

# Create a map
map = geemap.Map(center=[26, 87], zoom=8)
#map.to_streamlit()

'''draw = geemap.plugins.Draw(export=False)
draw.get_root().'''


Draw(export=True).add_to(map)
#c1, c2 = st.columns(2)
#with c1:
    #output = st_folium(map)

#with c2:
    #st.write(output['last_active_drawing']['geometry'])

output = st_folium(map,height=1000,width=600)
roi=output['last_active_drawing']['geometry']

#st.write(roi)
#Soil texture classes (USDA system) for 6 soil depths
if st.button('load_data'):
    soil_texture_image=ee.Image("OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02")
    soil_texture_viz = {
        'bands':['b10'],
        'min':1.0,
        'max':12.0,
        'palette':[
        'd5c36b','b96947','9d3706','ae868f','f86714','46d143',
        '368f20','3e5a14','ffd557','fff72e','ff5a9d','ff005b',
    ]
    }
    filtered_soil_texture=soil_texture_image.select('b10')
    reduced_soil_texture= filtered_soil_texture.reduceRegion(
        reducer=ee.Reducer.median(),
        geometry=roi,
        scale=10,
        maxPixels=1e10
        # Replace with the appropriate scale value
    ).getInfo()
    reduced_soil_texture['b10'] 
    soil_types={1:'clay',2:'silty_clay',3:'sandy_clay',4:'clay_loam',5:'clay_loam',6:'clay_loam',7:'loam',8:'silty_loam',9:'sandy_loam',10:'silty',11:'sandy_loam',12:'sandy'}
    soil_texture=soil_types[round(reduced_soil_texture['b10'])]
    map.addLayer(filtered_soil_texture,soil_texture_viz, 'Soil texture class (USDA system)')

    #Sand content in % (kg / kg) at 6 standard depths (0, 10, 30, 60, 100 and 200 cm) at 250 m resolution
    sand_content_image=ee.Image("OpenLandMap/SOL/SOL_SAND-WFRACTION_USDA-3A1A1A_M/v02")
    sand_content_viz = {
        'bands':['b10'],
        'min':1.0,
        'max':110.0,
        'palette':[
        'ffff00', 'f8f806', 'f1f10c', 'ebeb13', 'e4e419', 'dddd20',
        'd7d726', 'd0d02d', 'caca33', 'c3c33a', 'bcbc41', 'b6b647',
        'b0b04e', 'a9a954', 'a3a35a', '9c9c61', '959568', '8f8f6e',
        '898975', '82827b', '7b7b82', '757589', '6e6e8f', '686895',
        '61619c', '5a5aa3', '5454a9', '4d4db0', '4747b6', '4141bc',
        '3a3ac3', '3333ca', '2d2dd0', '2626d7', '2020dd', '1919e4',
        '1212eb', '0c0cf1', '0606f8', '0000ff',
    ]
    }
    filtered_sand_content=sand_content_image.select('b10')
    reduced_sand_content= filtered_sand_content.reduceRegion(
        reducer=ee.Reducer.median(),
        geometry=roi,
        scale=10,
        maxPixels=1e10
        # Replace with the appropriate scale value
    ).getInfo()
    sand_content=round(reduced_sand_content['b10'],2) #divide by 10 so that it can be for soil
    map.addLayer(filtered_sand_content,sand_content_viz, 'Sand content in % (kg / kg)')
        
    # Check if the user clicks the "show data" button

    #soil_ph content in the soil in terms of g/kg
    ph_image=ee.Image("OpenLandMap/SOL/SOL_PH-H2O_USDA-4C1A2A_M/v02")
    ph_viz = {
        'bands':['b10'],
        'min':42,
        'max':110,
        'palette': [
        'ff0000', 'ff1c00', 'ff3900', 'ff5500', 'ff7100', 'ff8e00',
        'ffaa00', 'ffc600', 'ffe200', 'ffff00', 'e3ff00', 'c7ff00',
        'aaff00', '8eff00', '72ff00', '55ff00', '39ff00', '1dff00',
        '01ff00', '00ff1c', '00ff38', '00ff54', '00ff71', '00ff8d',
        '00ffa9', '00ffc6', '00ffe2', '00fffe', '00e3ff', '00c7ff',
        '00abff', '008fff', '0072ff', '0056ff', '003aff', '001dff',
        '0001ff', '1b00ff', '3800ff', '5400ff',
    ]
    }
    filtered_ph=ph_image.select('b10')
    reduced_ph= filtered_ph.reduceRegion(
        reducer=ee.Reducer.median(),
        geometry=roi,
        scale=10,
        maxPixels=1e10
        # Replace with the appropriate scale value
    ).getInfo()
    reduced_ph['b10'] #divide by 10 so that it can be for soil
    soil_ph=round(reduced_ph['b10']/10,1)
    map.addLayer(filtered_ph,ph_viz, 'Soil pH x 10 in H2O')
    #carbon content in the soil in terms of g/kg Soil organic carbon content in x 5 g / kg
    carbon_content_image=ee.Image("OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02")
    clay_content_viz = {
        'bands':['b10'],
        'min': 2,
        'max':100,
        'palette': [
        'ffffa0','f7fcb9','d9f0a3','addd8e','78c679','41ab5d',
        '238443','005b29','004b29','012b13','00120b',
    ]
    }
    filtered_carbon_content=carbon_content_image.select('b10')
    reduced_carbon_content= filtered_carbon_content.reduceRegion(
        reducer=ee.Reducer.median(),
        geometry=roi,
        scale=10,
        maxPixels=1e10
        # Replace with the appropriate scale value
    ).getInfo()
    carbon_content=round(reduced_carbon_content['b10'],2)
    map.addLayer(filtered_carbon_content,clay_content_viz, 'clay_content in % (kg/kg)')
    #clay content in the soil
    clay_content_image=ee.Image("OpenLandMap/SOL/SOL_CLAY-WFRACTION_USDA-3A1A1A_M/v02")
    clay_content_viz = {
        'bands':['b10'],
        'min': 2,
        'max':100,
        'palette': [
        'ffff00', 'f8f806', 'f1f10c', 'ebeb13', 'e4e419', 'dddd20',
        'd7d726', 'd0d02d', 'caca33', 'c3c33a', 'bcbc41', 'b6b647',
        'b0b04e', 'a9a954', 'a3a35a', '9c9c61', '959568', '8f8f6e',
        '898975', '82827b', '7b7b82', '757589', '6e6e8f', '686895',
        '61619c', '5a5aa3', '5454a9', '4d4db0', '4747b6', '4141bc',
        '3a3ac3', '3333ca', '2d2dd0', '2626d7', '2020dd', '1919e4',
        '1212eb', '0c0cf1', '0606f8', '0000ff',
    ]
    }
    filtered_clay_content=clay_content_image.select('b10')
    reduced_clay_content= filtered_clay_content.reduceRegion(
        reducer=ee.Reducer.median(),
        geometry=roi,
        scale=10,
        maxPixels=1e10
        # Replace with the appropriate scale value
    ).getInfo()
    reduced_clay_content['b10']
    clay_content=round(reduced_clay_content['b10'],2)
    map.addLayer(filtered_clay_content,clay_content_viz, 'clay_content in % (kg/kg)')
    #bulk density of soil in kg/m^3

    bulk_density_image=ee.Image("OpenLandMap/SOL/SOL_BULKDENS-FINEEARTH_USDA-4A1H_M/v02")
    bulk_density_viz = {
        'bands':['b10'],
        'min': 5.0,
        'max':185.0,
        'palette': ['5e3c99', 'b2abd2', 'f7e0b2', 'fdb863', 'e63b01']
    }
    filtered_bulk_density=bulk_density_image.select('b10')
    reduced_bulk_density= filtered_bulk_density.reduceRegion(
        reducer=ee.Reducer.median(),
        geometry=roi,
        scale=10,
        maxPixels=1e10
        # Replace with the appropriate scale value
    ).getInfo()
    bulk_density=round(reduced_bulk_density['b10'],2)
    map.addLayer(filtered_bulk_density,bulk_density_viz, 'bulk_density in kg/m^3')

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
    soil_moisture=round(reduced_moisture['SoilMoi00_10cm_tavg']*100,2)# moisture in volume /volume %
    map.addLayer(filtered_moisture,moisture_viz, 'moisture Collection')
    #soil_temperature and it is in kelvin

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
    #collecting all the datat of soil from above code
    data=[{'sand_content':sand_content,'soil_texture':soil_texture,'carbon_content':carbon_content,'clay_content':clay_content,'soil_moisture':soil_moisture,'soil_temperature':soil_temperature,'soil_ph':soil_ph,'bulk_density':bulk_density}]
    environment2=pd.DataFrame(data)


    #api for temperrature and atmoshpheric condition
    long=roi['coordinates'][0][0][0]#longitude
    lati=roi['coordinates'][0][0][1]#latitud
    url=f'https://api.openweathermap.org/data/2.5/weather?lat={lati}&lon={long}&units=metric&appid=cbaf7470aa5e936d80f553bad7839eea'
    response=requests.post(url)
    json_data=response.json()
    wind_speed=json_data['wind']['speed']
    humidity=json_data['main']['humidity']
    temperature=json_data['main']['temp']
    weather_data=[{'temperature':temperature,'humidity':humidity,'wind_speed':wind_speed}]
    environment1=pd.DataFrame(weather_data)
    environment=pd.concat([environment1,environment2],axis=1)
    st.header('here is the data of of drawn polygon of soil')
    st.write(environment)
 
    