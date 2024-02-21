import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from functions.misc import *
from elements.route_anzeigen_overview import *

styles_css = read_styles()

def create_navbar(pages):
    # define nav bar to navigate between multiple pages
    navbar = dbc.NavbarSimple(
        children=[

                dbc.NavItem(dbc.NavLink(f"{page['name']}", href=page["relative_path"])) for page in pages

        ],
        brand="ANZEIGEN APP",
        color="primary",
        dark=True,
        style={'height':'20px'}
    )
    return navbar

def side_bar_collapsable():
    collapse = html.Div(
        [
            html.Div(
                dbc.Collapse(
                    html.Div(
                        dbc.Col([
                            dbc.Row([complete_search_box()]),
                            dbc.Row([load_previous_searches_div()])
                        ]),
                        style={"width": "400px"},
                    ),
                    id="horizontal-collapse",
                    is_open=False,
                    dimension="width"
                ),
                style={"minHeight": "100px", "width":"100%"},
            ),
        ]
    )
    return collapse



def content_element(pages):
    content = html.Div(
    id="page-content", children=[pages],
    style=styles_css["CONTENT_STYLE"])
    return content


