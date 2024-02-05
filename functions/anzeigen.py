import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import pandas as pd
import uuid
import time
from pprint import *

def new_article_json(name, img, url_ref, price, location, latitude, longitude, description, time_posted):
    return {
        'name':name,
        'img': img,
        'url_ref': url_ref,
        'price': price,
        'location_description': location,
        'latitude' : latitude,
        'longitude': longitude,
        'description': description,
        'time_posted': time_posted
    }
    
   
def add_article(json_file_path, article_obj): 
    if(os.path.isfile(json_file_path)):
        articles_df = pd.read_json(json_file_path)
        
        
        filtered_df = articles_df[(articles_df['latitude'] == article_obj['latitude']) & (articles_df['longitude'] == article_obj['longitude'])]
        if(len(filtered_df)>0):
            article_obj['latitude'] = article_obj['latitude'] + 0.01
            article_obj['longitude'] = article_obj['longitude'] + 0.01
        if(articles_df.empty):
            articles_df = pd.DataFrame([article_obj],ignore_index =True)
        else:
            if(len(articles_df[articles_df['url_ref'] == article_obj['url_ref']])== 0):
                articles_df = pd.concat([articles_df, pd.DataFrame([article_obj])], ignore_index=True)
    else:
        articles_df = pd.DataFrame([article_obj])

    articles_df.to_json(json_file_path)  



 
def search_anzeigen_everywhere(geolocator, json_file_path, search_input, page_limit):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
    }
    
    page_limit = int(page_limit)
    search_input = search_input.replace(" ","-")

    
    URL_ROOT = "https://www.kleinanzeigen.de"
    URL = "{root}{filter_price}/{search_phrase}/k0".format(root= URL_ROOT, filter_price="/s-preis:3000:4000", search_phrase=search_input)

    next_page_url = URL
    while(next_page_url != None):
        print(next_page_url)
        next_page_url = extract_article_all_page(geolocator, json_file_path, headers, URL_ROOT, next_page_url, page_limit)   
    

def extract_article_all_page(geolocator, json_file_path, headers, URL_ROOT, URL, page_limit):
    response = requests.get(url=URL, headers=headers)
    page = response.content
    soup = BeautifulSoup(page, "html.parser")
    srchRslts = soup.find_all("article")

    # Looped durch alle Search-Results durch.
    for srchRslt in srchRslts:
        for item in srchRslt.find_all("div"):
            if('aditem-main--top--left' in item.get('class')):
                location_desc = item.text.replace("\n ","")
                if(len(location_desc) > 100):
                    location_desc = location_desc.split("<")[0]
            if('aditem-main--top--right' in item.get('class')):
                time_posted = item.text.replace("\n ","")
                time_posted = time_posted.replace("  ","")
                
        for item in srchRslt.find_all("p"):
            if(item.get('class') != None):
                if('aditem-main--middle--price-shipping--price' in item.get('class')):
                    price = item.text.replace(" ","")
                    price = price.replace("\n","" )
                if( 'aditem-main--middle--description' in item.get('class')):
                    description = item.text.replace("\n", "")
                if( 'text-module-end' in item.get('class')):
                    text_module = item.text
        
        try: 
            name = srchRslt.find_all("a")[1].contents[0]
        except: 
            name = ''
        try:
            img = srchRslt.img['srcset']
        except:
            img = ''
        try:
            url = URL_ROOT  + srchRslt['data-href']
        except:
            url = ''
            
        location_obj = format_location_description(geolocator, location_desc)
        if(location_obj == None):
            latitude = None
            longitude = None
        else:
            latitude = location_obj.latitude
            longitude = location_obj.longitude
            
        article_obj = new_article_json(name, img , url , price, location_desc, latitude, longitude ,description, time_posted)
        add_article(json_file_path, article_obj)
        
    # Find Next Page 
    try:
        next_page = soup.find("a", {"class": "pagination-next"})        
        next_page_url =  "{root}{search_phrase}".format(root= URL_ROOT,search_phrase= next_page['href'])
        # if(next_page['href'].split(":")[1]> page_limit):
        #     next_page_url = None
    except:
        next_page_url = None
        
    return next_page_url    



def find_anzeigen_general_search(geolocator, search_phrases_list, page_limit):
    json_anzeigen = './data/anzeigen_general.json'
    if os.path.exists(json_anzeigen):
        os.remove(json_anzeigen)
    for search in search_phrases_list:
        print("Searching everywhere for" + search )
        search_anzeigen_everywhere(geolocator, json_anzeigen, search, page_limit)
        
def format_location_description(geolocator, loc_desc):
    location_arr = loc_desc.split(" ")
    try:
        location_g = geolocator.geocode(loc_desc)
        i=len(location_arr)
        while(location_g == None and i!=0):
            location_g = geolocator.geocode(location_arr[0:i-2])
            i = i-1
    except:
        print("FORMAT LOCATION ERROR " + str(loc_desc))
        location_g = None
        
    return location_g
























def extract_article_information_overview_page(geolocator, city_input, json_file_path, headers, URL_ROOT, URL, page_limit):
    
    response = requests.get(url=URL, headers=headers)
    page = response.content
    soup = BeautifulSoup(page, "html.parser")

    srchRslts = soup.find_all("article")

    # Looped durch alle Search-Results durch.
    for srchRslt in srchRslts:
        for item in srchRslt.find_all("div"):
            if('aditem-main--top--left' in item.get('class')):
                location_desc = item.text.replace("\n ","")
            if('aditem-main--top--right' in item.get('class')):
                time_posted = item.text.replace("\n ","")
                time_posted = time_posted.replace("  ","")
                
        for item in srchRslt.find_all("p"):
            if(item.get('class') != None):
                if('aditem-main--middle--price-shipping--price' in item.get('class')):
                    price = item.text.replace(" ","")
                    price = price.replace("\n","" )
                if( 'aditem-main--middle--description' in item.get('class')):
                    description = item.text.replace("\n", "")
                if( 'text-module-end' in item.get('class')):
                    text_module = item.text
        
        try: 
            name = srchRslt.find_all("a")[1].contents[0]
        except: 
            name = ''
        try:
            img = srchRslt.img['srcset']
        except:
            img = ''
        try:
            url = URL_ROOT  + srchRslt['data-href']
        except:
            url = ''
            
        location_obj = format_location_description(geolocator, location_desc)
        if(location_obj == None):
            latitude = None
            longitude = None
        else:
            latitude = location_obj.latitude
            longitude = location_obj.longitude
        article_obj = new_article_json(name, img , url , price, location_desc, latitude, longitude ,description, time_posted)
        add_article(json_file_path, article_obj)
        
    # Find Next Page 
    try:
        next_page = soup.find("a", {"class": "pagination-next"})        
        next_page_url =  "{root}/s-{city}{search_phrase}".format(root= URL_ROOT, city=city_input, search_phrase= next_page['href'])
        if(next_page['href'].split(":")[1]> page_limit):
            next_page_url = None
    except:
        next_page_url = None
        
    return next_page_url    

 
def search_anzeigen_in_location(geolocator, json_file_path, search_input, city_input, radius, page_limit):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
    }
    
    locationId =make_location_code_reference(headers, city_input)
    page_limit = int(page_limit)
    search_input = search_input.replace(" ","-")
    radius = radius.replace("km","")
    if(radius == '0'):
        radius = ''
    else:
        radius = 'r'+radius
    
    URL_ROOT = "https://www.kleinanzeigen.de"
    URL = "{root}/s-{city}/{search_phrase}/k0l{locationId}{radius}".format(root= URL_ROOT, city=city_input, search_phrase=search_input, locationId=locationId, radius=radius)

    next_page_url = URL
    while(next_page_url != None):
        print(next_page_url)
        next_page_url = extract_article_information_overview_page(geolocator, city_input, json_file_path, headers, URL_ROOT, next_page_url, page_limit)   
        
def make_location_code_reference(headers, postcode):
    URL = "https://www.kleinanzeigen.de/s-ort-empfehlungen.json?query={postcode}".format(postcode=postcode)
    response = requests.get(url=URL, headers=headers)
    page = response.content
    json_location_code = list(json.loads(page))    
    return json_location_code[0]


def find_anzeigen_along_route_individual_search(geolocator, search_radius, search_phrases_list, location_point_names, page_limit):
    search_radius.replace(" km", "")
    json_anzeigen = './data/anzeigen.json'
    if os.path.exists(json_anzeigen):
        os.remove(json_anzeigen)
    for search in search_phrases_list:
        previous_city = ''
        for loc in location_point_names:
            if(loc[1] == 'Deutschland'):
                city = str(loc[0])
                if(city != previous_city):
                    print("Searching " + search + "   in  "+ city)
                    search_anzeigen_in_location(geolocator, json_anzeigen, search, city, search_radius, page_limit)
                previous_city = city
                