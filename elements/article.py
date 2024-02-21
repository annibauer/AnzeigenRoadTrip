import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import pandas as pd
from functions.misc import *


styles_css = read_styles()


def article_card(article):
    card = dbc.Col([
        dbc.Card(id=str(article["location_description"]), children=[
            dbc.CardHeader(article["time_posted"]),
            dbc.CardBody([
                html.A([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([html.Img(src=article["img"])])
                        ], width=3),
                        dbc.Col([
                            dbc.Row(
                                [html.H4(article["name"], className="card-title")]),
                            dbc.Row([html.H6(article["description"])]),
                            dbc.Row([html.H3(article["price"])]),
                        ], width=9),
                    ])

                ], href=article["url_ref"], target="_blank")]),
        ])
    ], width=6, style=styles_css["article_card"])

    return card


def anzeigen_search():
    search_div = dbc.Card([
        dbc.Col([
            dbc.Row([
                html.H6('Search Anzeigen')
            ], style=styles_css["style_row_title"]),
            
            dbc.Row([
                
                dbc.Col([
                    dbc.Row([
                            dbc.ButtonGroup([
                                dbc.Button([html.I(className="bi bi-plus-square", style=styles_css["icon_size_add_remove"])],
                                           id='add_search_phrase_btn', n_clicks=0, style=styles_css["buttons_add_remove"]),
                                dbc.Button([html.I(className="bi bi-dash-square-dotted", style=styles_css["icon_size_add_remove"])],
                                           id='rm_search_phrase_btn', n_clicks=0, style=styles_css["buttons_add_remove"])
                            ], style=styles_css["buttons_add_remove_group"])
                ]),
                ], width=5),
                dbc.Col([
                    dbc.Row(id='search_inputs_div', children=[
                        dbc.Row([dcc.Input(
                            id='search_phrase_input', placeholder='Enter Search Phrase', style=styles_css["input_add_remove"])])
                    ], style={'height': '100%'}),
                ], width=7)
                
            ], style=styles_css["style_row_search"]),
            
            dbc.Row([
                
                dbc.Col([html.P('Price Range', style=styles_css["title_search"])], width=3),
                     dbc.Col([
                         dbc.Row([
                             dbc.Col([
                                 dcc.Input(
                                     id='price_range_min_input', placeholder='Enter Min', style=styles_css["input_prices"])
                             ]),
                             dbc.Col([
                                 dcc.Input(
                                     id='price_range_max_input', placeholder='Enter Max', style=styles_css["input_prices"])
                             ])
                         ])
                     ], width=9)
                     
            ], style=styles_css["style_row_search"]),
            
            dbc.Row([
                
                dbc.Col([html.P('Search Page Limit', style=styles_css["title_search"])], width=6),
                     dbc.Col([
                         dcc.Dropdown(id='dropdown_page_limit', options=[str(i) for i in range(
                             1, 101)], value=str(40), style={'width': '100%'}),
                     ], width=6)
                     
            ], style=styles_css["style_row_search"]),
            
            dbc.Row([
                
                dbc.Button("General Search", color="primary", n_clicks=0, className="me-1",
                    id='start_general_search_btn', style=styles_css["button_main"])
                
                ],style=styles_css["style_row_search"]),
            
            dbc.Row([
                
                dbc.Col([html.P('Search Radius Around Route', style=styles_css["title_search"])], width=6),
                     dbc.Col([
                         dcc.Dropdown(id='dropdown_radius', options=[
                                      '0 km', '5 km', '10 km', '20 km', '30 km', '40 km', '50 km', '60 km', '70 km', '80 km', '90 km', '100 km', '110 km', '120 km', '130 km', '140 km',  '150 km'], value='0 km', style={'width': '100%'}),
                     ], width=6)
                     
            ], style=styles_css["style_row_search"]),

            dbc.Row([
                dbc.Button("Search Along Route", color="primary", n_clicks=0,className="me-1", id='start_search_btn', style=styles_css["button_main"])
                ], style=styles_css["style_row_search"]),
            dbc.Row([
                html.Div(id="loading-calculate-route")
            ])
        ], style=styles_css["search_card_contents"])
    ], style=styles_css["search_card"])

    return search_div


def input_search_div(id_search_input):
    search_input = dbc.Row([dcc.Input(
        id=id_search_input, placeholder='Enter Search Phrase', style=styles_css["input_add_remove"])])
    return search_input
