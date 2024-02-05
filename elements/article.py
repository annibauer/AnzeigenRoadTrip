import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import pandas as pd


style_carousel = {'width': 'auto', 'justify': 'center', 'margin': '10px'}
style_row = {'justify': 'center'}
style_table_div = {'margin': '10px'}
style_table = {"width": "100%", "overflowX": "auto",
               'background-color': 'rgba(255, 255, 0, 0.5)', "color": "black"}
style_title_info = {'margin': '0px'}
style_header = {'fontWeight': 'bold', 'textAlign': 'center'}
style_cell = {'textAlign': 'left'}
style_card = {"font-size": "80%", "height": "100%"}
style_header = {'fontWeight': 'bold',
                'textAlign': 'center', 'padding-bottom': '20px'}


def article_card(article):
    card = dbc.Col([dbc.Card(id=str(article["url_ref"]), children=[
        dbc.CardHeader(article["time_posted"]),
        dbc.CardBody(
            [
                    dbc.Row([html.H4(article["name"], className="card-title")]),
                    dbc.Row([html.H3(article["location"])]),
                    dbc.Row([dcc.Link(article["url_ref"])]),
                    dbc.Row([html.Img(src=article["img"])])
                    ])
    ])
    ])

    return card


def anzeigen_search():
    search_div = dbc.Card([
        dbc.Col([
            dbc.Row([
                html.H5('Search Anzeigen')
            ], style=style_header),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "+", color="primary",  id='add_search_phrase_btn', n_clicks=0, style={'font-size': '70%'})
                        ], width=6),
                        dbc.Col([
                            dbc.Button(
                                "-", color="primary",  id='rm_search_phrase_btn', n_clicks=0, style={'font-size': '70%'})
                        ], width=6)
                    ], style={'width': 'auto', 'justify': 'center', 'margin-left': '20px', 'margin-right': '20px', 'height': '50px'}),
                ], width=4),
                dbc.Col([
                    dbc.Row(id='search_inputs_div', children=[
                        dbc.Row([dcc.Input(id='search_phrase_input', placeholder='Enter Search Phrase', style={
                            'margin-top': '10px', 'margin-bottom': '10px', 'height': '30px'})])
                    ], style={'height': '100%'}),
                ], width=8)
            ], style=style_header),
            dbc.Row([dbc.Col([html.H5('Price Range', style={'text-align': "left"})], width=6),
                     dbc.Col([
                         dbc.Row([
                                dbc.Col([
                                    dcc.Input(id='price_range_min_input', placeholder='Enter Min', style={
                                    'margin-top': '10px', 'margin-bottom': '10px', 'height': '30px','width':'80%'})
                                    ]),.
                                dbc.Col([
                                    dcc.Input(id='price_range_max_input', placeholder='Enter Max', style={
                                    'margin-top': '10px', 'margin-bottom': '10px', 'height': '30px', 'width':'80%'})                            
                                    ])
                         ])
                     ], width=6)
                     ], style=style_header),
            
            dbc.Row([dbc.Col([html.H5('Search Radius Around Route', style={'text-align': "left"})], width=6),
                     dbc.Col([
                         dcc.Dropdown(id='dropdown_radius', options=[
                                      '0 km', '5 km', '10 km', '20 km', '30 km', '40 km', '50 km'], value='0 km', style={'width': '100%'}),
                     ], width=6)
                     ], style=style_header),
            dbc.Row([dbc.Col([html.H5('Search Page Limit', style={'text-align': "left"})], width=6),
                     dbc.Col([
                         dcc.Dropdown(id='dropdown_page_limit', options=[str(i) for i in range(1,101)], value='100', style={'width': '100%'}),
                     ], width=6)
                     ], style=style_header),
            dbc.Row([dbc.Button("Start Route Search", color="primary", n_clicks=0, className="me-1",
                                id='start_search_btn')],style={'margin-bottom':'10px'}),
            dbc.Row([dbc.Button("Load Previous Search Results", color="primary", n_clicks=0, className="me-1",
                    id='load_search_results_btn')]),
        ], style={'padding': '30px', 'height':'100%'})
    ], style={'margin': '20px'})

    return search_div


def input_search_div(id_search_input):
    search_input = dbc.Row([dcc.Input(id=id_search_input, placeholder='Enter Search Phrase', style={
        'margin-top': '10px', 'margin-bottom': '10px', 'height': '30px'})])
    return search_input
