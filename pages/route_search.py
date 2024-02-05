import dash
from dash import Dash, html, dcc, html, Input, Output, callback, State, no_update
import pandas as pd
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import dash_bootstrap_components as dbc
import geocoder as gc
from pprint import pprint
import json
import os
from os import listdir
from os.path import isfile, join
import logging
from elements.article import *
from elements.route import route_div, input_route_div, route_map
from functions.maps import *
from functions.anzeigen import *
import geocoder
import pandas as pd

dash.register_page(__name__, path='/')

geolocator = Nominatim(user_agent="Anzeigen_App")

global m
global location_points 
m = folium.Map(location=[52, 7], tiles="OpenStreetMap", zoom_start=5)
m.save('map_og.html')

location_point_names = []
location_points = []

layout = html.Div([
    dbc.Row([
        dbc.Col([route_div()],width=6),
        dbc.Col([anzeigen_search()], width=6)
    ]),
    dbc.Row([
        dbc.Col([route_map()], width=12)
    ])
],style={'textAlign': 'center', 'padding':'10px','margin':'20px'})


@callback([
    Output("calculate_route_btn", "n_clicks"),
    Output("add_waitpoint_btn", "n_clicks"),
    Output("rm_waitpoint_btn", "n_clicks"),
    Output("waypoint_inputs_div", "children"),
    Output("map_route_div", "children"),
    Output("start_search_btn", "n_clicks"),
    Output("add_search_phrase_btn", "n_clicks"),
    Output("rm_search_phrase_btn", "n_clicks"),
    Output("search_inputs_div", "children"),
    Output("load_route_btn", "n_clicks"),
    Output("load_search_results_btn", "n_clicks"),
    ], [Input("calculate_route_btn", "n_clicks"),
        Input("add_waitpoint_btn", "n_clicks"),
        Input("rm_waitpoint_btn", "n_clicks"),
        Input("start_search_btn", "n_clicks"),
        Input("add_search_phrase_btn", "n_clicks"),
        Input("rm_search_phrase_btn", "n_clicks"),
        Input("load_route_btn", "n_clicks"),
        Input("load_search_results_btn", "n_clicks"),
        State("start_loc_input","value"),
        State("end_loc_input","value"),
        State("waypoint_inputs_div","children"),
        State("search_inputs_div","children"),
        State("dropdown_radius","value"),
        State("dropdown_page_limit","value")
        ], 
)
def route_calculation(n_calculate_route, n_add_waypoints, n_rm_waypoints, n_start_search, n_add_searchphrase, n_rm_searchphrase, n_load_route, n_load_search_results, start_loc_input, end_loc_input, waypoint_div, search_phrases_div, search_radius, page_limit):
    global m
    global location_point_names 
    global location_points 
    
    map_div = html.Iframe(id='map', srcDoc=open('map_og.html', 'r').read(), width="100%", height="600px")
    search_radius = search_radius.replace(" km", "")
    # calculate button pressed
    if n_calculate_route != 0:
        
        # start and end point declared
        if((start_loc_input != '' and start_loc_input != None) and (end_loc_input != '' and end_loc_input != None)):
            print("calculate route")
            waypoints = format_dynamic_inputs(waypoint_div)
                    
            # complete route
            complete_route = []
            complete_route.append(start_loc_input)
            complete_route.extend(waypoints)
            complete_route.append(end_loc_input)
            route_text = ''
            for stop in complete_route:
                route_text = route_text +  "-> " + str(stop)
            
            # GET ROUTE 
            #location_point_names, location_points = generate_route_postcodes(geolocator,complete_route)     
            location_points = generate_route_coordinates(geolocator,complete_route)            
            html_file_name = 'map_route.html'
            map_div, m = generate_map_route(location_points, html_file_name)

            print("calculated route {text}".format(text=route_text))
            logging.info("calculate route {text}".format(text=route_text))

    # add way points 
    if(n_add_waypoints !=0):
        waypoint_div.append(input_route_div("way_point_{}".format(len(waypoint_div)+1)))
        
    # add way points 
    if(n_rm_waypoints !=0):
        print("remove")
        if(len(waypoint_div)!=0):
            waypoint_div.pop(-1)

    # calculate button pressed
    if n_start_search != 0:
        print("START SEARCH")
        search_phrases_list = format_dynamic_inputs(search_phrases_div)
        if(len(search_phrases_list) != 0 and len(location_points) != 0):
            #find_anzeigen_along_route_individual_search(geolocator, search_radius, search_phrases_list, location_point_names, page_limit)
            find_anzeigen_general_search(geolocator, search_phrases_list, page_limit)
        
        route_anzeigen_json = './data/anzeigen_route.json'
        if os.path.exists(route_anzeigen_json):
            os.remove(route_anzeigen_json)
        articles_df = pd.read_json('./data/anzeigen_general.json')
        for index, article in articles_df.iterrows():
            article_location = {
                'desc':article['location_description'],
                'latitude': article['latitude'],
                'longitude': article['longitude']
            }
            html_file_name = 'map_route_adds.html'
            if(check_if_anzeige_on_route(location_points, [article_location['latitude'],article_location['longitude']], search_radius)):
                pprint("ARTICLE ON ROUTE")
                pprint(article['name'])
                add_article(route_anzeigen_json, article)
                map_div, m = add_location_anzeigen_markers_to_map(article, article_location, m ,html_file_name)
            
        
        print("Search Done. ")
        
    # calculate button pressed
    if n_load_search_results != 0: 
        route_anzeigen_json = './data/anzeigen_route.json'
        if os.path.exists(route_anzeigen_json):
            os.remove(route_anzeigen_json)
        articles_df = pd.read_json('./data/anzeigen_general.json')
        for index, article in articles_df.iterrows():
            print(article['location_description'])
            article_location = {
                'desc':article['location_description'],
                'latitude': article['latitude'],
                'longitude': article['longitude']
            }
            html_file_name = 'map_route_adds.html'
            if(check_if_anzeige_on_route(location_points, [article_location['latitude'],article_location['longitude']], search_radius)):
                add_article(route_anzeigen_json, article)
                map_div, m = add_location_anzeigen_markers_to_map(article, article_location, m ,html_file_name)
        
        print("Loading Done")
        
        
    # calculate button pressed
    if n_load_route != 0: 
        route_df = pd.read_json('./data/route.json')
        location_points = route_df[['latitude','longitude']].values.tolist()
        if(len(location_points)!= 0):        
            map_div, m = generate_map_route(location_points, 'map_route.html')
        

        
    # add way points 
    if(n_add_searchphrase !=0):
        search_phrases_div.append(input_search_div("searchphrase_{}".format(len(search_phrases_div)+1)))
        
    # add way points 
    if(n_rm_searchphrase !=0):
        print("remove")
        if(len(search_phrases_div)!=0):
            search_phrases_div.pop(-1)


    n_calculate_route = 0
    n_add_waypoints = 0
    n_rm_waypoints = 0
    n_start_search = 0
    n_add_searchphrase = 0 
    n_rm_searchphrase = 0
    n_load_search_results = 0
    n_load_route = 0
    return [n_calculate_route, n_add_waypoints, n_rm_waypoints, waypoint_div, map_div, n_start_search, n_add_searchphrase, n_rm_searchphrase, search_phrases_div, n_load_search_results, n_load_route]
    
    
 