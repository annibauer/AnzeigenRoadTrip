import dash
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from functions.logger import configure_logger
from elements.article import *
from elements.route import *
from elements.main_page import create_navbar
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

#logger = configure_logger()

# Create a logs directory if it doesn't exist
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Configure logging to use TimedRotatingFileHandler
log_filename = os.path.join(log_dir, 'app.log')
handler = TimedRotatingFileHandler(log_filename, when='midnight', interval=1, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger()
logger.addHandler(handler)

# Set up main app 
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUX, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True)

# navbar = create_navbar(dash.page_registry.values())

# set main page layout
app.layout = html.Div([
    #navbar,
    dash.page_container
])


if __name__ == '__main__':
    app.run(debug=True)
