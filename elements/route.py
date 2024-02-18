import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import pandas as pd
import geocoder
from functions.misc import *


styles_css = read_styles()


def route_div():
    route_div = dbc.Card([
        dbc.Col([
            dbc.Row([
                html.H6('Select Route')
            ], style=styles_css["style_row_search"]),
            dbc.Row([dbc.Col([html.P('Start Point', style=styles_css["title_search"])], width=6),
                     dbc.Col([
                         dcc.Input(id='start_loc_input', value=geocoder.ip(
                             'me').city, placeholder='Enter Starting Location Name', style={'width': '90%'})
                     ], width=6)
                     ], style=styles_css["style_row_search"]),
            dbc.Row([
                dbc.Col([
                        dbc.Row([
                            dbc.ButtonGroup([
                                dbc.Button([html.I(className="bi bi-plus-square", style=styles_css["icon_size_add_remove"])],
                                           id='add_waitpoint_btn', n_clicks=0, style=styles_css["buttons_add_remove"]),
                                dbc.Button([html.I(className="bi bi-dash-square-dotted", style=styles_css["icon_size_add_remove"])],
                                           id='rm_waitpoint_btn', n_clicks=0, style=styles_css["buttons_add_remove"])
                            ], style=styles_css["buttons_add_remove_group"])
                        ]),
                        ], width=5),
                dbc.Col([
                        dbc.Row(id='waypoint_inputs_div', children=[
                            dbc.Row([dcc.Input(
                                id='search_phrase_input', placeholder='Enter Waypoint', style=styles_css["input_add_remove"])])
                        ], style={'height': '100%'}),
                        ], width=7)
            ], style=styles_css["style_row_search"]),

            dbc.Row([
                dbc.Col(
                    [html.P('Destination', style=styles_css["title_search"])], width=6),
                dbc.Col([
                    dcc.Input(id='end_loc_input', placeholder='Enter End Location Name', style={
                        'width': '90%'})
                ], width=6)
            ], style=styles_css["style_row_search"]),
            dbc.Row([

                dbc.Button("Calculate Route", color="primary", n_clicks=0,  className="me-1",
                           id='calculate_route_btn', style=styles_css["button_main"])
            ], style=styles_css["style_row_search"]),

        ], style=styles_css["search_card_contents"]),
    ], style=styles_css["search_card"])

    return route_div


def route_map():
    div = dbc.Card([
        dbc.Row(id='map_route_div', children=[])
    ], style=styles_css["map"])
    return div


def input_route_div(id_way_point_loc_input):
    way_point_input = dbc.Row([dcc.Input(
        id=id_way_point_loc_input, placeholder='Enter Way Point', style=styles_css["input_add_remove"])])
    return way_point_input

def loading_element():
    dcc.Loading(
        id="loading-1",
        type="default",
        children=html.Div(id="loading-output-1")
    )