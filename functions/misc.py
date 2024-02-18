import json


def read_settings():
    # JSON file
    f = open ('settings.json', "r")
    # Reading from file
    data_settings = json.loads(f.read())
    
    return data_settings


def read_styles():
    data_settings = read_settings()
    # JSON file
    f = open (data_settings['styles'], "r")
    # Reading from file
    data_style_css = json.loads(f.read())
    
    return data_style_css


def compound_paths(settings):
    json_route = settings["route_folder"] + settings["route_file"] 
    route_anzeigen_json = settings["search_data_folder"] + settings["along_route_filtered_results"] 
    anzeigen_general_json = settings["search_data_folder"] + settings["general_search_results"]
    html_map_route = settings["map_folder"] + settings["map_with_route"]
    html_map_route_anzeigen = settings["map_folder"] + settings["map_with_route_anzeigen"] 
    
    return json_route, route_anzeigen_json, anzeigen_general_json, html_map_route, html_map_route_anzeigen
      