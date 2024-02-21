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
from elements.main_page import *
import geocoder
import pandas as pd
from functions.misc import *
from functions.feature_functions import *
from elements.route import *



styles_css = read_styles()

dash.register_page(__name__, path='/')

geolocator = Nominatim(user_agent="Anzeigen_App")
settings = read_settings()
json_route, route_anzeigen_json, anzeigen_general_json, html_map_route, html_map_route_anzeigen = compound_paths(settings)

global m
global ROUTE_LOADED
global SEARCH_ALONG_ROUTE_DISABLED

m = create_empty_map(settings)
ROUTE_LOADED = False
SEARCH_ALONG_ROUTE_DISABLED = True

layout = dbc.Col([
    dbc.Row([
        dbc.Col([
            dbc.Row([
            dbc.Button(
                "Search Settings",
                id="horizontal-collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
                style=styles_css["search_settings_btn"]
            )]),
            dbc.Row([
                dcc.Loading(
                    id="loading-general",
                    type="default",
                    children=html.Div(id="loading-output-general"),
                ),
            ], style={'margin':"10px"})
        ])
        ], style={"margin":"10px"}),
    dbc.Row([
        dbc.Col([side_bar_collapsable()], id="collapsable_col", style={"display":"none"}),
        dbc.Col([
            dbc.Row([route_map()]),
            dbc.Row([modal_load_previous_search()])
            ], id='content_col', width=12)
        ],style={"margin":"10px", "height":"100%"}),
    dbc.Row([],style={"height":"50px"}),
    dbc.Row([html.H5(id="results_anzeigen", children=[], style={"color":"#f06b05"})], style={"margin":"30px"}),
    dbc.Row([dbc.Col(id='table_anzeigen', children=[], style={"margin":"20px"})
    ])
    
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
    Output("results_anzeigen", "children"),
    Output('loading-search-route', 'children'),
    Output('loading-calculate-route', 'children'),
    Output('loading-general', 'children'),
    Output('start_search_btn', 'disabled'),
    Output("horizontal-collapse", "is_open"),
    Output("collapsable_col", "style"),
    Output("content_col", "width"),
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
        State("table_anzeigen","children"),
        State("horizontal-collapse", "is_open"),
        State("collapsable_col", "style"),
        State("content_col", "width"),
        State("results_anzeigen", "children")
        ], 
)
def route_calculation(n_calculate_route, n_add_waypoints, n_rm_waypoints, n_start_search, n_add_searchphrase, n_rm_searchphrase, n_load_route, n_load_search_results, n_load_general_search_results, start_loc_input, end_loc_input, waypoint_div, search_phrases_div, search_radius, page_limit, price_min, price_max, table_anzeigen_div, is_open, width_collapsable, width_content, anzeigen_results_info):
    global m
    global ROUTE_LOADED
    global SEARCH_ALONG_ROUTE_DISABLED
    
    map_div = create_map_div(settings)
    
    loading_output_calculate_route = []
    loading_output_search_route = []
    loading_general = []
    search_phrases_div, n_add_searchphrase, n_rm_searchphrase = trigger_format_dynamic_inputs(n_add_searchphrase ,n_rm_searchphrase, search_phrases_div, input_search_div, "searchphrase")
    waypoint_div, n_add_waypoints, n_rm_waypoints = trigger_format_dynamic_inputs(n_add_waypoints ,n_rm_waypoints, waypoint_div, input_route_div, "way_point")
          
        # calculate button pressed
    if n_calculate_route != 0: 
        logging.info("Calculate route button pressed.")
        map_div, m, route_text = calculate_route(geolocator, start_loc_input, end_loc_input,waypoint_div,json_route ,html_map_route)
        loading_output_calculate_route = html.Div([
            html.Div("Route Loaded: {}".format(route_text), style={'color':'green'})
        ])
        loading_general = html.Div([
            html.Div()
        ])
        
        ROUTE_LOADED = True
        SEARCH_ALONG_ROUTE_DISABLED = not ROUTE_LOADED
        n_calculate_route = 0

        
    elif n_start_search != 0:
        logging.info("Route search button pressed.")

        if(os.path.exists(json_route)):
            table_anzeigen_div, map_div, m, search_phrases, count_articles_on_route = start_search_anzeigen(geolocator, m, search_phrases_div, page_limit, price_min, price_max, search_radius, html_map_route_anzeigen,json_route, route_anzeigen_json, anzeigen_general_json)
       
        anzeigen_results_info = "{} Anzeigen found on route".format(count_articles_on_route)

        loading_output_search_route = html.Div([
            dbc.Col([
                dbc.Row([html.Div("Results Along Route Loaded:  Radius {radius} km  Page Limit {page_limit}".format(radius=search_radius, page_limit=page_limit), style={'color':'green'})]),
                dbc.Row([html.Div("Search Terms:  {search_term}".format(search_term=search_phrases), style={'color':'green'})])
            ])
            
        ])
        loading_general = html.Div([
            html.Div()
        ])
        
        if(is_open):
            width_content = 12
            width_collapsable = {"display":"none"}
            is_open = not is_open
        else:
            width_content = 8
            width_collapsable = {"display":"block"}
            is_open = not is_open
            

        n_start_search = 0
        
    # load search results button pressed
    elif n_load_search_results != 0: 
        logging.info("Load previous route search button pressed.")
        if os.path.exists(route_anzeigen_json):
            table_anzeigen_div, map_div, m, count_articles_on_route = load_search_anzeigen_along_route(m, html_map_route_anzeigen, route_anzeigen_json)
            anzeigen_results_info = "{} Anzeigen found on route ".format(count_articles_on_route)
        n_load_search_results = 0
        
    # calculate button pressed
    elif n_load_general_search_results != 0: 
        logging.info("Load general search button pressed.")
        loading_output_search_route = html.Div([
            dcc.Loading(type="circle", fullscreen=True),
        ])
        if (os.path.exists(anzeigen_general_json) and os.path.exists(json_route)):
            table_anzeigen_div, map_div, m, count_articles_on_route = load_general_search(json_route, html_map_route, search_radius, html_map_route_anzeigen, route_anzeigen_json, anzeigen_general_json)
            anzeigen_results_info = "{} Anzeigen found in Deutschland ".format(count_articles_on_route)
            
        n_load_general_search_results = 0
        
    elif n_load_route != 0:
        logging.info("Load previous route pressed.")
        if(os.path.exists(json_route)):
            map_div, m  = load_route(json_route, html_map_route)
            
        ROUTE_LOADED = True
        SEARCH_ALONG_ROUTE_DISABLED = not ROUTE_LOADED
        n_load_route = 0
    
  
              
    return [n_calculate_route, n_add_waypoints, n_rm_waypoints, n_start_search, n_add_searchphrase, n_rm_searchphrase,n_load_route, n_load_search_results, n_load_general_search_results, waypoint_div, search_phrases_div, map_div,  table_anzeigen_div, anzeigen_results_info, loading_output_calculate_route, loading_output_search_route, loading_general, SEARCH_ALONG_ROUTE_DISABLED, is_open, width_collapsable, width_content]
    
    

@callback(
    Output("horizontal-collapse", "is_open", allow_duplicate=True),
    Output("collapsable_col", "style", allow_duplicate=True),
    Output("content_col", "width", allow_duplicate=True),
    [Input("horizontal-collapse-button", "n_clicks")],
    [State("horizontal-collapse", "is_open"),
        State("collapsable_col", "style"),
        State("content_col", "width")],
    prevent_initial_call=True
)
def toggle_collapse(n, is_open, width_collapsable, width_content):
    
    if n:
        if(is_open):
            width_content = 12
            width_collapsable = {"display":"none", "height":"100%"}
        else:
            width_content = 8
            width_collapsable = {"display":"block","height":"100%"}
            
        return not is_open, width_collapsable, width_content
    

    
    return is_open, width_collapsable, width_content



@callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open
