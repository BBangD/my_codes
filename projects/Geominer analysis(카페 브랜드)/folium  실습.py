# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import folium
import numpy as np
import json
import requests
import pandas as pd
import branca

# +

m = folium.Map(location=[37.56642229866859, 126.97797397798712])
m

# -

m.save('map.html')

folium.Map(location=[37.56642229866859, 126.97797397798712], tiles='Stamen Toner', zoom_start=15)

#marker
m=folium.Map(location=[37.56642229866859, 126.97797397798712], tiles='Stamen Toner', zoom_start=15
          )
tooltip = "click me!"
folium.Marker([37.565682651272645, 126.96633639034327], popup = '<b> seodaemun station', tooltip=tooltip
             ).add_to(m)
folium.Marker([37.559915554959744, 126.96475841219394], popup = '<b> Chungjungro station', tooltip=tooltip
             ).add_to(m)
m

# +
#아이콘
m=folium.Map(location=[37.56642229866859, 126.97797397798712], zoom_start=12
          )
tooltip = "click me!"
folium.Marker([37.565682651272645, 126.96633639034327], popup = '<b> seodaemun station', 
              icon = folium.Icon(color='red',icon = 'info-sign')       ).add_to(m)
folium.Marker([37.559915554959744, 126.96475841219394], popup = '<b> Chungjungro station', 
              icon = folium.Icon(color='green',icon = 'bookmark')      ).add_to(m)
folium.Marker([37.55980761490468, 126.94239825094982], popup = '<b> Sinchon station', 
              icon = folium.Icon(color='blue',icon = 'flag')      ).add_to(m)
 
m

# +
from folium import plugins

m=folium.Map(location=[37.56642229866859, 126.97797397798712], zoom_start=12
          )
tooltip = "click me!"
folium.Marker([37.565682651272645, 126.96633639034327], popup = '<b> seodaemun station', 
              icon = folium.Icon(color='red',icon = 'info-sign')       ).add_to(m)
icon_plane = plugins.BeautifyIcon(icon='plane', border_color  = 'darkblue',text_color = 'darkblue',
                                 icon_shape = 'circle')
icon_flag = plugins.BeautifyIcon(icon='flag', border_color  = 'green',text_color = 'green',
                                 icon_shape = 'triangle')
icon_number = plugins.BeautifyIcon(number=10, border_color  = 'darkred',text_color = 'darkred',
                                 inner_icon_style = 'margin-top;0')
folium.Marker([37.559915554959744, 126.96475841219394], popup = '<b> Chungjungro station', 
              icon = folium.Icon(color='green',icon = 'bookmark')      ).add_to(m)
folium.Marker([37.55980761490468, 126.94239825094982], popup = '<b> Sinchon station', 
              icon = folium.Icon(color='blue',icon = 'flag')      ).add_to(m)
folium.Marker([37.5597225540901, 126.80344299796681], popup = 'Plane', 
              icon = icon_plane      ).add_to(m)
folium.Marker([37.56378780702765, 126.81745485753298], popup = 'Number', 
              icon = icon_number      ).add_to(m)
folium.Marker([37.57383817359705, 126.88450488706529], popup = 'Flag', 
              icon = icon_flag      ).add_to(m)
m

# +
# 보트 마커
m = folium.Map([30,-180], zoom_start=3)
plugins. BoatMarker(
    location=(38.35101128054379, 129.53821815027683),
    heading = 45, wind_heading =45 ,wind_speed=45,
    color= 'purple' ).add_to(m)

plugins. BoatMarker(
    location=(37.590874825871325, 131.79826492700184),
    heading = -20, wind_heading =120 ,wind_speed=45,
    color= 'darkblue' ).add_to(m)

plugins. BoatMarker(
    location=(35.834101401014024, 134.09339260934055),
    heading = -30, wind_heading =25 ,wind_speed=80,
    color= 'green').add_to(m)
m

# +
#클릭마커
m = folium.Map(location=[37.54595583197816, 126.89286716403456],
              tiles = 'Stamen Terrain', zoom_start =13)

folium.Marker([37.556190317414604, 126.97252991409236], popup='Seoul Station').add_to(m)
m.add_child(folium.ClickForMarker(popup='Marker'))
m

# +
#circle
#아이콘
m=folium.Map(location=[37.56642229866859, 126.97797397798712], zoom_start=12
          )
tooltip = "click me!"
folium.Circle([37.565682651272645, 126.96633639034327], popup = '<b> seodaemun station', 
              color='red',radius = 60, fill=False       ).add_to(m)
folium.CircleMarker([37.559915554959744, 126.96475841219394], popup = '<b> Chungjungro station', 
              color='darkblue',radius = 40,fill=True,fill_color='darkblue'  ).add_to(m)
folium.CircleMarker([37.55980761490468, 126.94239825094982], popup = '<b> Sinchon station', 
             color='purple',radius=20, fill_color='purple'     ).add_to(m)
 
m

# +
cities = [[37.566687, 126.978417], [35.179774, 129.075004], [37.455900, 126.705522],[35.871380, 128.601743],
          [36.350451, 127.384827],[35.160072, 126.851440]]
m = folium.Map(location = [36.74045757540965, 128.05798951265768],tiles = 'Stamen Terrain', zoom_start=7)

for i in range(len(cities)):
    folium.CircleMarker(location=cities[i],
                 radius=10,
                 color='red').add_to(m)
m
# -

m = folium.Map(location = [36.74045757540965, 128.05798951265768], zoom_start=7)
folium.PolyLine(locations = cities, tooltip='PolyLine').add_to(m)
m

m = folium.Map(location = [36.74045757540965, 128.05798951265768], zoom_start=7)
folium.Rectangle(bounds = cities, tooltip='Rectangle').add_to(m)
m

m = folium.Map(location = [36.74045757540965, 128.05798951265768], zoom_start=7)
folium.Polygon(locations = cities,fill=True, tooltip='Polygon').add_to(m)
m

# +
#PolyLineTextPath
m = folium.Map(location=[37,127], zoom_start=5)
wind_positions = [[35.48892793905415, 132.33542398256563],[35.91364272886096, 128.89853526204195]
                 ,[37.02941852079097, 125.34423729951284],[35.83580357228896, 120.21025084042722]]
wind_line = folium.PolyLine(wind_positions,weight=20,color = 'deepskyblue').add_to(m)

plugins.PolyLineTextPath(wind_line,') ',repeat=True,offset = 7, attributes={'fill': ' dodgerblue', 'font-weight' : 'bold',
                                                                           'font-size' : 24}).add_to(m)
m
# -

#팝업
m = folium.Map(location=[37.56108386573351, 127.03042837335123], zoom_start = 13)
m.add_child(folium.LatLngPopup())
m

#팝업
m = folium.Map(location=[37.56108386573351, 127.03042837335123], zoom_start = 7)
html = """
    <h1>Seoul</h1><br>
    <p>
    Seoul, officially the Seoul Special City, is the capital and largest metropolis of South Korea
    </p>
    <a href = 'https://en.wikipedia.org/wiki/Seoul' target = _blank>wikipedia</a>
    """
folium.Marker([37.56108386573351, 127.03042837335123], popup = html).add_to(m)
m

#팝업
#팝업
m = folium.Map(location=[37.56108386573351, 127.03042837335123], zoom_start = 7)
df = pd.DataFrame(data = [[2000,9879000],[2010,9796000],[2020,9963000]], columns = ['Year', 'Pop'])
html = df.to_html(classes = 'table table-striped table-hover table-condensed table-responsive')
folium.Marker([37.56108386573351, 127.03042837335123], popup = html).add_to(m)
m

# +
#팝업
m = folium.Map(location=[37.56108386573351, 127.03042837335123], zoom_start = 4)
f = branca.element.Figure()
m = folium.Map(location=[37.56108386573351, 127.03042837335123], zoom_start = 7).add_to(f)
iframe = branca.element.IFrame(width = 500, height=300)
f.add_to(iframe)

popup = folium.Popup(iframe, max_width=2650)



folium.Marker([37.56108386573351, 127.03042837335123], popup = popup).add_to(m)
m
# -

from folium import plugins
N = 100
data = np.array([np.random.uniform(low = 35.5, high = 37.5, size = N),
                np.random.uniform(low = 127, high = 129, size = N),]).T
popups = [str(i) for i in range(N)]
m = folium.Map([36.5,128], zoom_start = 8)
plugins.MarkerCluster(data, popups = popups).add_to(m)
m

pip install vincent

# +
import vincent
scatter_points = {
    'x' : np.random.randn(50).cumsum(),
    'y' : np.random.randn(50).cumsum(),
}

scatter_chart = vincent.Scatter(scatter_points,iter_idx = 'x', width =400,height=200)
scatter_json = scatter_chart.to_json()
scatter_dict = json.loads(scatter_json)

m=folium.Map([36.5,128], zoom_start=7)
popup = folium.Popup()
folium.Vega(scatter_chart, height=250).add_to(popup)
folium.Marker([36,128], popup = popup).add_to(m)

popup = folium.Popup()
folium.Vega(scatter_json, height=250).add_to(popup)
folium.Marker([37,128], popup = popup).add_to(m)

popup = folium.Popup()
folium.Vega(scatter_dict, height=250).add_to(popup)
folium.Marker([36.5,127.5], popup = popup).add_to(m)
m

# +
url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
vis1 = json.loads(requests.get(f'{url}/vis1.json').text)
vis2 = json.loads(requests.get(f'{url}/vis2.json').text)
vis3 = json.loads(requests.get(f'{url}/vis3.json').text)

m=folium.Map(location = [47.3489,-124.708], zoom_start=7, tiles = 'Stamen Terrain')
folium.Marker([47.3489, -124.708], popup = folium.Popup(max_width=450 ).add_child(
folium.Vega(vis1,width=450,height=250))).add_to(m)

folium.Marker([44.639, -124.5339], popup = folium.Popup(max_width=450 ).add_child(
folium.Vega(vis2,width=450,height=250))).add_to(m)

folium.Marker([46.216, -124.1280], popup = folium.Popup(max_width=450 ).add_child(
folium.Vega(vis3,width=450,height=250))).add_to(m)

m

# +
from folium import plugins
m = folium.Map(location = [37.543531303548164, 126.95080944496473], zoom_start = 15)

lines = [{'coordinates' : [[126.95080944496473,37.543531303548164],
                           [126.98661263678777,37.5351279773759 ],],'dates' :['2020-01-01T00:00:00','2020-01-01T00:10:00'],
         'color' : 'red' },
        {'coordinates' : [[126.98661263678777,37.5351279773759],
                           [126.96742212576262,37.52901793758402 ],],'dates' :['2020-01-01T00:00:00','2020-01-01T00:20:00'],
         'color' : 'green' },
        {'coordinates' : [[126.96742212576262,37.52901793758402],
                           [126.97183307912057,37.544803075728666],],'dates' :['2020-01-01T00:00:00','2020-01-01T00:30:00'],
         'color' : 'blue', 'weight' : 10 },
        {'coordinates' : [[126.97183307912057,37.544803075728666],
                           [126.95080944496473,37.543531303548164],],'dates' :['2020-01-01T00:00:00','2020-01-01T00:40:00'],
         'color' : 'black' }]
features = [
        {'type' : 'Feature', 'geometry' : {
         'type' : 'LineString',
         'coordinates' : line['coordinates']
        }, 'properties' : {
            'times' : line['dates'], 'style' : {'color' : line['color'], 'weight' : line['weight'] if 'weight' in line else 5}
        }} for line in lines
]
plugins.TimestampedGeoJson({
    'type' : 'FeatureCollection',
    'features' : features
    
}, period = 'PT1M', add_last_point=True).add_to(m)
m
# -

m = folium.Map(location = [37,128], tiles = 'OpenStreetMap', zoom_start=4)
m

# +
from folium.plugins import MousePosition

m = folium.Map()
MousePosition().add_to(m)

m

# +
m = folium.Map()
formatter = "function(num) { return L.Util.formatNum(num,3);};"
MousePosition(
    position = 'topright',
    separator = ' | ',
    empty_string = 'NaN',
    lng_fitst = True, 
    num_digits = 20,
    prefix = 'Coordinates: ',
    lat_formatter = formatter,
    lng_formatter = formatter
).add_to(m)


m

# +
#terminator

m = folium.Map(zoom_start =1)
plugins.Terminator().add_to(m)
m

# +
from folium.plugins import MeasureControl

m = folium.Map([36.5,127], zoom_start = 10)
m.add_child(MeasureControl())

# +
from folium.plugins import Draw

m = folium.Map()
draw = Draw()
draw.add_to(m)
m

# +
#group
m = folium.Map(location = [0,0], zoom_start=6)

gs = folium.FeatureGroup(name = 'Groups')
m.add_child(gs)
g1 = plugins.FeatureGroupSubGroup(gs, 'Group1')
m.add_child(g1)
g2 = plugins.FeatureGroupSubGroup(gs, 'Group2')
m.add_child(g2)

folium.Marker([-2,-2]).add_to(g1)
folium.Marker([2,2]).add_to(g1)
folium.Marker([-2,2]).add_to(g2)
folium.Marker([2,-2]).add_to(g2)
folium.LayerControl(collapsed=False).add_to(m)

m
# -

m = folium.plugins.DualMap(location=[37,127], zoom_start=9)
m

# +
m = folium.plugins.DualMap(location=[37,127],tiles = None, zoom_start=9)

folium.TileLayer('OpenStreetMap').add_to(m.m1)
folium.TileLayer('CartoDBPositron').add_to(m.m2)
folium.LayerControl(collapsed=False).add_to(m)
m
# -

m = folium.plugins.DualMap(location=[37,127], zoom_start=9)
fg_both = folium.FeatureGroup(name = 'Markers Both').add_to(m)
fg_1 = folium.FeatureGroup(name = 'Markers 1').add_to(m.m1)
fg_2 = folium.FeatureGroup(name = 'Markers 2').add_to(m.m2)
icon_red = folium.Icon(color='red')
folium.Marker((37.5,127), tooltip = 'Both', icon = icon_red).add_to(fg_both)
folium.Marker((37,127.5), tooltip = '1',  icon = icon_red).add_to(fg_1)
folium.Marker((36.5,127), tooltip = '2',  icon = icon_red).add_to(fg_2)
folium.LayerControl(collapsed=False).add_to(m)
m

url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
state_geo = f'{url}/us-states.json'
state_unemployment = f'{url}/US_Unemployment_Oct2012.csv'
state_data = pd.read_csv(state_unemployment)
state_data

from branca.colormap import linear
colormap = linear.YlGnBu_09.scale(
    state_data.Unemployment.min(),
    state_data.Unemployment.max()
)
colormap

state_data_dict = state_data.set_index('State')['Unemployment']
state_data_dict['AL']

m = folium.Map([43,-100], zoom_start=4)
folium.GeoJson(state_geo, name = 'unemployment',
              style_function = lambda feature :{
                  'fillColor' : colormap(state_data_dict[feature['id']]),
                  'color' : 'black',
                  'weight' : 1,
                  'dashArray':'5, 5',
                  'fillOpacity':0.6
              }).add_to(m)
m

# +
m = folium.Map([43,-100], zoom_start=4)
folium.Choropleth(
    geo_data = state_geo,
    data = state_data,
    columns = ['State','Unemployment'],
    key_on = 'feature.id',
    fill_color='YlGnBu',
    fill_opacity = 0.6,
    line_opacity=0.2,
    legend_name = 'Unemployment Rate (%)'
).add_to(m)
folium.LayerControl().add_to(m)

m

# +
bins = list(state_data['Unemployment'].quantile([0,0.25,0.5,0.75,1]))
m = folium.Map([43,-100], zoom_start=4)
folium.Choropleth(
    geo_data = state_geo,
    data = state_data,
    columns = ['State','Unemployment'],
    key_on = 'feature.id',
    fill_color='YlOrBr',
    fill_opacity = 0.6,
    line_opacity=0.2,
    legend_name = 'Unemployment Rate (%)',
    bins=bins
).add_to(m)
folium.LayerControl().add_to(m)

m

# +
url = ' https://raw.githubusercontent.com/suanlab/dataset/master'
seoul_geo = f'{url}/seoul_municipalities_geo_simple.json'

seoul_data = pd.read_csv('seoul_population.csv', encoding = 'utf-8')
seoul_data

# +
m = folium.Map(
        location=[37.52455146239674, 126.97878909663497],
    zoom_start = 10
)

folium.GeoJson(
    json.loads(requests.get(seoul_geo).text),
    name = 'seoul_municipalities'
).add_to(m)

m
# -

colormap = linear.Blues_09.scale(
    seoul_data.population.min(),
    seoul_data.population.max()
)
colormap

population_dict = seoul_data.set_index('name')['population']
color_dict = {str(key): colormap(population_dict[key]) for key in population_dict.keys()}

# +
m = folium.Map(
        location=[37.52455146239674, 126.97878909663497],
    zoom_start = 11
)

folium.GeoJson(
     json.loads(requests.get(seoul_geo).text),
    name = 'population',
    style_function = lambda feature: {
        'fillColor' : color_dict[feature['properties']['name']],
        'color':'black',
        'weight':1,
        'dashArray':'5, 5',
        'fillOpacity':0.6,
        
    }
).add_to(m)

colormap.caption = 'Population color scale'
colormap.add_to(m)

folium.LayerControl().add_to(m)

m


# +
m = folium.Map(
        location=[37.52455146239674, 126.97878909663497],
    zoom_start = 11
)

folium.Choropleth(
     geo_data = json.loads(requests.get(seoul_geo).text),
    data = seoul_data,
    columns = ['name','population'],
    key_on = 'properties.name',
    fill_color = 'Blues',
    fill_opacity=0.6,
    line_opacity=0.4,
    legend_name = 'Population'
    
        
    
).add_to(m)



folium.LayerControl().add_to(m)

m

