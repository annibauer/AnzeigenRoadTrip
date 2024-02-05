import requests
import json
from pprint import *
import osmapi as osm
from geopy.geocoders import Nominatim
import geocoder
import folium
import pandas as pd
import dash
from dash import Dash, html, dcc, html, Input, Output, callback, State, no_update
import pandas as pd
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import dash_bootstrap_components as dbc
import os
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def location_formatting_request(geolocator, locations_array):
    locations_str = ''
    for location_name in locations_array:
        location = geolocator.geocode(location_name)
        loc_str = "{long},{lat};".format(long=location.longitude, lat=location.latitude)
        locations_str = locations_str + loc_str

    locations_str[-1] = ""
    return locations_str
    
def format_route_string(geolocator, route_array):
    route_string = ''
    for place in route_array:
        location_g = geolocator.geocode(place)
        lat = location_g.latitude
        long = location_g.longitude
        if(route_array.index(place) == len(route_array)-1):
            str_loc = "{long},{lat}".format(lat=lat,long=long)
        else:
            str_loc = "{long},{lat};".format(lat=lat,long=long)
        route_string = route_string + str_loc
    
    return route_string
    

def generate_route_coordinates(geolocator, route_array):
    route_string = format_route_string(geolocator, route_array)
    
    response = requests.get(url="http://router.project-osrm.org/route/v1/driving/{route_string}?alternatives=false&overview=simplified&annotations=nodes".format(route_string=route_string))
    json_data = json.loads(response.text)
    nodes = json_data['routes'][0]['legs'][0]['annotation']['nodes']
    step_size = round(len(nodes)/50)
    location_nodes = nodes[0::step_size]

    api = osm.OsmApi()
    location_points = []
    # location_point_names = []
    # postcodes_list = []
    # country_list = []
    latitude_list = []
    longitude_list = []
    for node in location_nodes:
        node = api.NodeGet(node)
        # location = geolocator.reverse("{lat},{lon}".format(lat=node['lat'], lon=node['lon']))
        # loc_address = location.raw['address']
        # try:
        #     postcode = loc_address['postcode']
        # except:
        #     postcode = loc_address['city']
        # country = loc_address['country']
        # postcodes_list.append(postcode)
        # country_list.append(country)
        latitude_list.append(node['lat'])
        longitude_list.append(node['lon'])
        
        # location_point_names.append([postcode,country])
        location_points.append([node['lat'],node['lon']])
    
    #route_df = pd.DataFrame(columns=['postcode','country','latitude','longitude'])
    route_df = pd.DataFrame(columns=['latitude','longitude'])
    # route_df['postcode'] = postcodes_list
    # route_df['country'] = country_list
    route_df['latitude'] = latitude_list
    route_df['longitude'] = longitude_list
            
    json_file_path = './data/route.json'
    if os.path.exists(json_file_path):
        os.remove(json_file_path)
    
    route_df.to_json(json_file_path)  
    # return location_point_names, location_points
    return location_points
    
def generate_map_route(location_points, html_file_name):
    m = folium.Map(location=[52, 15], tiles="OpenStreetMap", zoom_start=5)
    
    if(type(location_points)==list):
        item_past = location_points[0]
        for item in location_points[1:-1:3]:
            line = folium.PolyLine([item_past, item], weight=5, opacity=1)
            line.add_to(m)
            item_past = item
    if(type(location_points)==type(pd.DataFrame())):
        for index, row in location_points.iterrows():
            if(index == 0):
                item_past = [row['latitude'], row['longitude']]
            else:
                item = [row['latitude'], row['longitude']]
                line = folium.PolyLine([item_past, item], weight=5, opacity=1)
                line.add_to(m)
                item_past = item
        
    m.save(html_file_name)
    map_div =  html.Iframe(id='map', srcDoc=open(html_file_name, 'r').read(), width="100%", height="600px")
    return map_div, m

def format_dynamic_inputs(div_element):
    #extract way points entered
    points = []
    for item in div_element:
        for prop_item in item['props']['children']:
            try:
                points.append(prop_item['props']['value'])
            except:
                continue
    return points
    

def add_location_anzeigen_markers_to_map(article_df_row, location_g, m ,html_file_name):
    lat = location_g['latitude']
    long = location_g['longitude']
    
    card_article = folium.Html(
        """
        <div style="border: 1px solid #ccc; border-radius: 8px; overflow: hidden; width: 300px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
        <a href={url} target="_blank" style="text-decoration: none; color: inherit;">
        <img src={imgsrc} alt="Product Image" style="width: 100%; height: 200px; object-fit: cover;">
        <div style="padding: 16px;">
            <div style="font-size: 1.2em; margin-bottom: 8px;">{name}</div>
            <div style="color: #666; margin-bottom: 12px;">{location_desc}</div>
            <div style="font-weight: bold; color: #333;">{price}</div>
            <div style="color: #666; margin-bottom: 12px;">{time}</div>
        </div>
        </a>
        </div>
        """.format(name=article_df_row['name'], imgsrc=article_df_row["img"], price=article_df_row["price"], location_desc=article_df_row["location_description"], url=article_df_row["url_ref"], time= article_df_row["time_posted"])
        , script=True)
    
    popup = folium.Popup(card_article, max_width=2650)
    markers = folium.Marker([lat,long],popup=popup)
    markers.add_to(m)

    m.save(html_file_name)
    map_div =  html.Iframe(id='map', srcDoc=open(html_file_name, 'r').read(), width="100%", height="600px")
    return map_div, m


def calculate_distance(location1, location2):
    if location1 and location2:
        return geodesic(location1, location2).kilometers
    else:
        return None

def check_if_anzeige_on_route(route_coordinates_list, anzeige_cor, radius_around_route):
    ANZEIGE_NEAR_ROUTE = False
    for route_cor in route_coordinates_list:
        try:
            distance = calculate_distance(route_cor, anzeige_cor)
            if(distance <= float(radius_around_route)):
                ANZEIGE_NEAR_ROUTE = True
        except:
            print('not accurate coordinates  ' + str(anzeige_cor) + '   '+ str(route_cor) )


    return ANZEIGE_NEAR_ROUTE
