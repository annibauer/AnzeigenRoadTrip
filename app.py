import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime
from elements.article import *
from elements.route import *

# Create a logs directory if it doesn't exist
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Configure logging to use TimedRotatingFileHandler
log_filename = os.path.join(log_dir, 'app.log')
handler = TimedRotatingFileHandler(log_filename, when='midnight', interval=1, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger()
logger.addHandler(handler)

style_home_header={'margin':'10px', 'padding':'10px'}
style_home_links = {'margin:': '10px', 'padding':'10px'}

# Set up main app 
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUX, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True)

# define nav bar to navigate between multiple pages
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink(f"{page['name']}", href=page["relative_path"])) for page in dash.page_registry.values()
    ],
    brand="ANZEIGEN APP",
    color="primary",
    dark=True,
    style={'height':'15px'}
)

# set main page layout
app.layout = html.Div([
    navbar,
    dash.page_container
])


if __name__ == '__main__':
    app.run(debug=True)
