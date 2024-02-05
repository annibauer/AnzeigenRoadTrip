import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import pandas as pd
import geocoder


style_carousel = {'width': 'auto', 'justify': 'center', 'margin': '10px'}
style_row = {'justify': 'center'}
style_table_div = {'margin': '10px'}
style_table = {"width": "100%", "overflowX": "auto",
               'background-color': 'rgba(255, 255, 0, 0.5)', "color": "black"}
style_title_info = {'margin': '0px'}
style_header = {'fontWeight': 'bold',
                'textAlign': 'center', 'padding-bottom': '20px'}
style_cell = {'textAlign': 'left'}
style_card = {"font-size": "80%", "height": "100%"}


def route_div():
    route_div = dbc.Card([
        dbc.Col([
            dbc.Row([dbc.Col([html.H5('Start Point', style={'text-align': "left"})], width=6),
                     dbc.Col([
                         dcc.Input(id='start_loc_input', value=geocoder.ip(
                             'me').city, placeholder='Enter Starting Location Name', style={'width': '90%'})
                     ], width=6)
                     ], style=style_header),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "+", color="primary",  id='add_waitpoint_btn', n_clicks=0, style={'font-size': '70%'})
                        ], width=6),
                        dbc.Col([
                            dbc.Button(
                                "-", color="primary",  id='rm_waitpoint_btn', n_clicks=0, style={'font-size': '70%'})
                        ], width=6)
                    ], style={'width': 'auto', 'justify': 'center', 'margin-left': '20px', 'margin-right': '20px', 'height': '50px'}),
                ], width=4),
                dbc.Col([
                    dbc.Row(id='waypoint_inputs_div', children=[],
                            style={'height': '100%'}),
                ], width=8)
            ], style=style_header),
            dbc.Row([dbc.Col([html.H5('Destination', style={'text-align': "left"})], width=6),
                     dbc.Col([
                         dcc.Input(id='end_loc_input', placeholder='Enter End Location Name', style={
                             'width': '90%'})
                     ], width=6)
                     ], style=style_header),
            dbc.Row([dbc.Button("Calculate Route", color="primary", n_clicks=0,  className="me-1",
                                id='calculate_route_btn')], style={'margin-bottom':'10px'}),
            dbc.Row([dbc.Button("Load Previous Route", color="primary", n_clicks=0, className="me-1",
                    id='load_route_btn')]),
        ], style={'padding': '30px'})

    ], style={'margin': '20px'})

    return route_div


def route_map():
    div = dbc.Card([
        dbc.Row(id='map_route_div', children=[])
    ], style={'margin': '20px', 'padding': '20px'})

    return div


def input_route_div(id_way_point_loc_input):
    way_point_input = dbc.Row([dcc.Input(id=id_way_point_loc_input, placeholder='Enter Way Point', style={
                              'margin-top': '10px', 'margin-bottom': '10px', 'height': '30px'})])
    return way_point_input
