import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import pandas as pd
import geocoder
from functions.misc import *
from elements.article import *
from elements.route import route_div


styles_css = read_styles()


def load_previous_searches_div():
        
    div = dbc.Card([dbc.ButtonGroup(children=[
        dbc.Button("Previous Route", outline=True, color="primary", n_clicks=0, id='load_route_btn', style=styles_css["button_load"]),
        dbc.Button("Previous Route Article Results", outline=True, color="primary", n_clicks=0,  id='load_search_results_btn', style=styles_css["button_load"]),
        dbc.Button("Previous Search Phrase", outline=True, color="primary", n_clicks=0, id='load_general_search_results_btn', style=styles_css["button_load"]),
        ], style=styles_css["load"])
                    ],style=styles_css["load_card"])
    return div


def complete_search_box():  
    search_div = dbc.Col([
        dbc.Row([
            anzeigen_search(),
            ]),
        dbc.Row([
            route_div() 
        ])
    ])
    return search_div
