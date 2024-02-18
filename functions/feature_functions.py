import logging
from functions.anzeigen import *
from functions.maps import *
from functions.misc import *  

def trigger_format_dynamic_inputs(n_add ,n_rm, div, input, id_pre_desc):  
    logging.debug("Format Dynamic Input")
    
    # add points 
    if(n_add !=0):
        logging.debug("Add {id_pre_desc}".format(id_pre_desc=id_pre_desc))
        div.append(input("{desc}_{num}".format(num=len(div)+1, desc=id_pre_desc)))
        
    # add points 
    if(n_rm !=0):
        logging.debug("Remove {id_pre_desc}".format(id_pre_desc=id_pre_desc))
        if(len(div)!=0):
            div.pop(-1)  
                     
    n_add = 0
    n_rm = 0       
    return div, n_add, n_rm

def calculate_route(geolocator, start_loc_input, end_loc_input,waypoint_div,json_route ,html_map_route):

    # start and end point declared
    if((start_loc_input != '' and start_loc_input != None) and (end_loc_input != '' and end_loc_input != None)):
        print("calculate route")
        
        waypoints = format_dynamic_inputs(waypoint_div)
        complete_route, route_text = format_route_points_string(start_loc_input, waypoints, end_loc_input)
        location_points = generate_route_coordinates(geolocator, complete_route, json_route)            
        map_div, m = generate_map_route(location_points, html_map_route)

        print("calculated route {text}".format(text=route_text))
        logging.info("calculate route {text}".format(text=route_text))
            
    return  map_div, m
          
def start_search_anzeigen(geolocator, m ,search_phrases_div, page_limit, price_min, price_max, search_radius, html_map_route_anzeigen,json_route, route_anzeigen_json, anzeigen_general_json):  
    search_radius = search_radius.replace(" km", "")
    search_phrases_list = format_dynamic_inputs(search_phrases_div)
    route_df = pd.read_json(json_route)
    location_points = route_df[['latitude','longitude']].values.tolist()
    
    if(len(search_phrases_list) != 0 and len(location_points) != 0):
        find_anzeigen_general_search(geolocator, search_phrases_list, page_limit, price_min, price_max, anzeigen_general_json)

    table_anzeigen_div, map_div, m  = filter_on_route_anzeigen(location_points,search_radius, m, html_map_route_anzeigen, route_anzeigen_json, anzeigen_general_json)
    print("Search Done. ")
        
    return table_anzeigen_div, map_div, m

def load_search_anzeigen_along_route(m, html_map_route_anzeigen, route_anzeigen_json):
    table_anzeigen_div, map_div, m = display_filtered_anzeigen_map(m, html_map_route_anzeigen, route_anzeigen_json)
    print("Loading Done")
    return table_anzeigen_div, map_div, m

def load_general_search(json_route, html_map_route, search_radius, html_map_route_anzeigen, route_anzeigen_json, anzeigen_general_json):
    
    route_df = pd.read_json(json_route)
    location_points = route_df[['latitude','longitude']].values.tolist()
    if(len(location_points)!= 0):  
        map_div, m = generate_map_route(location_points, html_map_route)
        table_anzeigen_div, map_div, m  = display_filtered_anzeigen_map(m, html_map_route_anzeigen, anzeigen_general_json)

    return table_anzeigen_div, map_div, m

def load_route(json_route, html_map_route):
    route_df = pd.read_json(json_route)
    location_points = route_df[['latitude','longitude']].values.tolist()
    if(len(location_points)!= 0):  
        map_div, m = generate_map_route(location_points, html_map_route)

    return map_div, m