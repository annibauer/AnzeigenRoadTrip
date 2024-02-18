import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

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
