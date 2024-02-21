import dash
from dash import Dash, html, dcc, html, Input, Output, callback, State, no_update


def create_map_div(settings):
    map_div = html.Iframe(id='map', srcDoc=open(settings["map_folder"] + settings["empty_map"], 'r').read(), width="100%", height="800px")
    return map_div