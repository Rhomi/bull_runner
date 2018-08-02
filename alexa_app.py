# Essential imports
from flask import Flask, request #import main Flask class and request object
from flask_ask import Ask, statement
from bs4 import BeautifulSoup
import requests
import pyttsx3
import re
import sys
import os
import json
# word to number conversion
from word2number import w2n
# Find similarity beween strings
from difflib import SequenceMatcher

main_url = "https://www.usfbullrunner.com"
route_map_file = 'route_map.txt'

def http_request(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    source = requests.get(url, headers=headers).text
    return(BeautifulSoup(source, "html.parser"))
	

# This function is to get all get route info dynamically. Will be run when the app
# is installed for the first time and every time there is an update in the route map.
def get_all_routes(soup):
    all_routes = {}
    items = soup.find_all('li')
    for item in items:
        mini_url = item.find('a').attrs['href']
        route_name = item.find('a').text.lower().replace('route','').strip()
        route_url = main_url+mini_url
        all_routes[''+route_name] = route_url
    return(all_routes)
	
def get_route_map(all_routes):
    # create a route map dictionary from the routes dictionary
    # We will update the values in this dictionary with a dictionary of stop names and 
    # corresponding url.
    # route_map = dict.fromkeys(all_routes.keys(), 0)
    routes_list = list(all_routes.keys())
    entire_routes = []
    for url in all_routes.values():
        soup = http_request(url)
        # Get all the stops for a given route. They are all in a-href tags
        stops = soup.find_all('a')
        stops.pop(0)
        stop_names = []
        stop_url = []
        for stop in stops:
            stop_names.append(stop.text.lower())
            stop_url.append(main_url+stop.attrs['href'])
        entire_routes.append(dict(zip(stop_names, stop_url)))
    route_map = dict(zip(routes_list, entire_routes))
    return(route_map)
	
def interpret_response(response, match):
    no_arrivals_message = 'Arrival predictions are not available at this time'
    try:
        if response.text.lower().strip('.') == no_arrivals_message.lower():
            return(no_arrivals_message)
        else:
            # find the bus number that is returned as part of the reponse
            bus_number = re.findall(r"\D(\d{4})\D", response.text)
            # The bus_number is of type list. But a list of one element. Hence we need to replace only bus[0] with an empty string
            # This is for our final message
            return("At "+match+" the "+response.text.replace(bus_number[0], ""))
    except:
        return("Oops. Something went wrong")
 
def find_similarity(a, b):
    return (b,SequenceMatcher(None, a, b).ratio())

def get_next_bus(route, stop, all_routes):
	print(stop)
	if route in all_routes: # check if the bus name is in the keys of the dictionary
	# This is s regex way of doing things.
	# find out how many mathces the stop searched for has in the selected route using regex
	#   regex=re.compile(".*"+str(stop)+".*")
	#   matches = [m.group(0) for l in all_routes[route] for m in [regex.search(l)] if m]
	# Let's add more intelligence to the app.
		stop_ratios = [find_similarity(stop,stop_name) for stop_name in all_routes[route]]
		stops = [x[0] for x in stop_ratios]
		ratios = [x[1] for x in stop_ratios]
		best_match = stops[ratios.index(max(ratios))]

		if best_match:
			final_message = "Your search matches one stop. "
			stop_url = all_routes[route][best_match]
			soup = http_request(stop_url)
			body = soup.find_all('li')
			final_message = final_message+interpret_response(body[1], best_match)
			return(final_message)
		else:
			return("The stop " + best_match.title() + " is not available in route " + route.title() + ". Please check the stop name or update the route map.")
	else:
		return("Oops. That's an invalid route name")
	
def update_route_map(route_map_file):
    url = 'https://www.usfbullrunner.com/simple/routes'
    soup = http_request(url)
    all_routes = get_all_routes(soup)    
    with open(route_map_file, 'w') as f:
        f.write(json.dumps(get_route_map(all_routes)))
		

def read_route_map(route_map_file):
    with open(route_map_file, 'r') as f:
        route_map = json.load(f)
    return(route_map)
	
def preprocessing(route, stop):
    if route in ['lib express','library express','library']:
        route = 'lib express'
    if route in ['marshall student center express', 'msc express', 'marshall express', 'student center express', 'msc']:
        route = 'msc express'
    if stop in ['msc']:
        stop = 'marshall student center'
    try:
        stop = w2n.word_to_num(str(stop))
        print('Hello', stop)
    except:
        stop = stop
    return(str(route),str(stop))

def say_it(final_message):
    engine = pyttsx3.init()
    if type(final_message) is list:
        for  message in final_message:
            engine.say(message)
            engine.runAndWait()
    else:
        engine.say(final_message)
        engine.runAndWait()
    
def process_request(route, stop):
    route,stop = preprocessing(route.lower(),stop.lower())

    # There is a possibility for stops to be of type int after preprocessing (example Stop 504 on Route F)
    print("You have requested timings for route " + route + " and " + str(stop))
    if not os.path.exists(route_map_file):
        update_route_map(route_map_file)		
    try:    
        route_map = read_route_map(route_map_file)
        final_message = get_next_bus(route, stop, route_map)
        print(final_message)
        return(final_message)
        #say_it(final_message)

	# Exception handling for empty route map file or unreadable content in the file.
	# Update the file and read it again
    except ValueError as e:    
        try: 
            update_route_map(route_map_file)
            route_map = read_route_map(route_map_file)
            final_message = get_next_bus(route, stop, route_map) 

        except Exception as e:
            print(e)
            final_message = "Oops. Something went wrong with the initialization. Please try again."    
            say_it(final_message)
    # One final message for the arrival predictions as well as errors.
    
if __name__ == "__main__":
    main()


    # We need to match the stop name/ or part of the stop name to route map -keys.