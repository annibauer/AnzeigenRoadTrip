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
from elements.maps import *
import geocoder
import pandas as pd
from functions.misc import *
from functions.feature_functions import *
from elements.route import *

dash.register_page(__name__, path='/')

geolocator = Nominatim(user_agent="Anzeigen_App")
settings = read_settings()
json_route, route_anzeigen_json, anzeigen_general_json, html_map_route, html_map_route_anzeigen = compound_paths(settings)

global m

m = create_empty_map(settings)

layout = dbc.Col([
    dbc.Row([
        dbc.Col([
                complete_search_box()
            ], width=4),
        dbc.Col([
            dbc.Row([route_map()]),
            dbc.Row([load_previous_searches_div()]),
            dbc.Row([
                  loading_element()
            ])
        ], width=8)

    ], style=styles_css["main_layout_rows"]),    
    dbc.Row([
        dbc.Col(id='table_anzeigen', children=[
            ], width=12)
    ], style=styles_css["main_layout_rows"])
],style={'textAlign': 'center', 'padding':'10px','margin':'20px'})


@callback([
    Output("calculate_route_btn", "n_clicks"),
    Output("add_waitpoint_btn", "n_clicks"),
    Output("rm_waitpoint_btn", "n_clicks"),
    Output("start_search_btn", "n_clicks"),
    Output("add_search_phrase_btn", "n_clicks"),
    Output("rm_search_phrase_btn", "n_clicks"),
    Output("load_route_btn", "n_clicks"),
    Output("load_search_results_btn", "n_clicks"),
    Output("load_general_search_results_btn", "n_clicks"),
    Output("waypoint_inputs_div", "children"),
    Output("search_inputs_div", "children"),
    Output("map_route_div", "children"),
    Output("table_anzeigen", "children"),
    ], [Input("calculate_route_btn", "n_clicks"),
        Input("add_waitpoint_btn", "n_clicks"),
        Input("rm_waitpoint_btn", "n_clicks"),
        Input("start_search_btn", "n_clicks"),
        Input("add_search_phrase_btn", "n_clicks"),
        Input("rm_search_phrase_btn", "n_clicks"),
        Input("load_route_btn", "n_clicks"),
        Input("load_search_results_btn", "n_clicks"),
        Input("load_general_search_results_btn", "n_clicks"),
        State("start_loc_input","value"),
        State("end_loc_input","value"),
        State("waypoint_inputs_div","children"),
        State("search_inputs_div","children"),
        State("dropdown_radius","value"),
        State("dropdown_page_limit","value"),
        State("price_range_min_input","value"),
        State("price_range_max_input","value"),
        State("table_anzeigen","children")
        ], 
)
def route_calculation(n_calculate_route, n_add_waypoints, n_rm_waypoints, n_start_search, n_add_searchphrase, n_rm_searchphrase, n_load_route, n_load_search_results, n_load_general_search_results, start_loc_input, end_loc_input, waypoint_div, search_phrases_div, search_radius, page_limit, price_min, price_max, table_anzeigen_div):
    global m
    map_div = create_map_div(settings)
    
    search_phrases_div, n_add_searchphrase, n_rm_searchphrase = trigger_format_dynamic_inputs(n_add_searchphrase ,n_rm_searchphrase, search_phrases_div, input_search_div, "searchphrase")
    waypoint_div, n_add_waypoints, n_rm_waypoints = trigger_format_dynamic_inputs(n_add_waypoints ,n_rm_waypoints, waypoint_div, input_route_div, "way_point")
          
        # calculate button pressed
    if n_calculate_route != 0: 
        logging.info("Calculate route button pressed.")
        map_div, m = calculate_route(geolocator, start_loc_input, end_loc_input,waypoint_div,json_route ,html_map_route)
        n_calculate_route = 0
        
    elif n_start_search != 0:
        logging.info("Route search button pressed.")
        if(os.path.exists(json_route)):
            table_anzeigen_div, map_div, m = start_search_anzeigen(geolocator, m, search_phrases_div, page_limit, price_min, price_max, search_radius, html_map_route_anzeigen,json_route, route_anzeigen_json, anzeigen_general_json)
        n_start_search = 0
        
    # load search results button pressed
    elif n_load_search_results != 0: 
        logging.info("Load previous route search button pressed.")
        if os.path.exists(route_anzeigen_json):
            table_anzeigen_div, map_div, m = load_search_anzeigen_along_route(m, html_map_route_anzeigen, route_anzeigen_json)
        n_load_search_results = 0
        
    # calculate button pressed
    elif n_load_general_search_results != 0: 
        logging.info("Load general search button pressed.")
        if (os.path.exists(anzeigen_general_json) and os.path.exists(json_route)):
            table_anzeigen_div, map_div, m = load_general_search(json_route, html_map_route, search_radius, html_map_route_anzeigen, route_anzeigen_json, anzeigen_general_json)
        n_load_general_search_results = 0
        
    elif n_load_route != 0:
        logging.info("Load previous route pressed.")
        if(os.path.exists(json_route)):
            map_div, m  = load_route(json_route, html_map_route)
        n_load_route = 0
    
  
              
    return [n_calculate_route, n_add_waypoints, n_rm_waypoints, n_start_search, n_add_searchphrase, n_rm_searchphrase,n_load_route, n_load_search_results, n_load_general_search_results, waypoint_div, search_phrases_div, map_div,  table_anzeigen_div]
    
    
@callback(Output("loading-output-1", "children"), Input("load_general_search_results_btn", "n_clicks"))
def input_triggers_spinner(value):
    print("Hello")
    time.sleep(1)
    return value