# IGS Boston 
# Kevin Coakley (June 2020)
# Yelp API Search Program

# API syntax information available at 'https://api.yelp.com/v3/businesses/search'

# Import modules
import requests
import json
import csv
import math

# Go to 'https://www.yelp.com/developers/documentation/v3/authentication'
# Register app with Yelp to get API key
# Enter API key
API_KEY = 'xxx'
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

# Function - Write to CSV
# Note - Set Location (Python Directory) to folder where have output csv file
def write_csv(business_data):
    try:
        with open("output1.csv", "a", newline="\n") as file: # Change output file each time run program
            c = csv.writer(file)
            counter = 1

            for i in business_data['businesses']:
                if not i['categories']:
                    print("Skipping entry", counter, "- does not have category info")
                    counter += 1
                else: 
                    c.writerow([i['name'],
                    i['rating'],
                    i['phone'],
                    i['id'],
                    i['alias'],
                    i['categories'][0]['title'],
                    i['review_count'],
                    i['url'],
                    i['coordinates']['latitude'],
                    i['coordinates']['longitude'],
                    i['location']['city'],
                    i['location']['state'],
                    i['location']['zip_code'],
                    i['location']['country'],
                    i['location']['address1'],
                    i['location']['address2'],
                    i['location']['address3'],
                    i['distance']])
                    counter += 1
            print("Successful Write to CSV")

    except:
        print("Error - Failed to Write")

# Function - Location Search
def location_search(query_type, query, location, radius):
    PARAMETERS = {query_type: query,
              'limit': 50,
              'offset': 0,
              'radius': radius,
              'location': location}
    response = requests.get(url = ENDPOINT,
                        params = PARAMETERS,
                        headers = HEADERS)
    business_data = response.json()
    print("\n****************************************************")
    print("Results found for", query_type, query,":", business_data['total'], "within", radius, "meters\n")
    results_count = business_data['total']
    rounded = math.ceil(results_count/50)
    print("Iterations required for", query_type, query, ":", rounded, "\n")
    for i in range(rounded):
        if i < 20:
            offset = i * 50
            PARAMETERS = {query_type: query,
                    'limit': 50,
                    'offset': offset,
                    'radius': radius,
                    'location': location}
            response = requests.get(url = ENDPOINT,
                                params = PARAMETERS,
                                headers = HEADERS)
            business_data = response.json()
            print("Writing records",offset + 1, "to", offset + 50, ".....", end = '')
            write_csv(business_data)
        else: 
            print("\nStopped writing records at 1,000 of", results_count,"\nYelp API limits to 1,000 results per query. Consider narrowing search radius or query.")
            break
    print("\nCompleted search.")
    print("****************************************************\n")


# Function - Latitude / Longitude Search
def latlong_search(query_type, query, latitude, longitude, radius):
    PARAMETERS = {query_type: query,
              'limit': 50,
              'offset': 0,
              'radius': radius,
              'latitude': latitude,
              'longitude': longitude}
    response = requests.get(url = ENDPOINT,
                        params = PARAMETERS,
                        headers = HEADERS)
    business_data = response.json()
    print("\n****************************************************")
    print("Results found for", query_type, query,":", business_data['total'], "within", radius, "meters\n")
    results_count = business_data['total']
    rounded = math.ceil(results_count/50)
    print("Iterations required for", query_type, query, ":", rounded, "\n")
    for i in range(rounded):
        if i < 20:
            offset = i * 50
            PARAMETERS = {query_type: query,
                    'limit': 50,
                    'offset': offset,
                    'radius': radius,
                'latitude': latitude,
                'longitude': longitude}
            response = requests.get(url = ENDPOINT,
                                params = PARAMETERS,
                                headers = HEADERS)
            business_data = response.json()
            print("Writing records",offset + 1, "to", offset + 50, ".....", end = '')
            write_csv(business_data)
        else: 
            print("\nStopped writing records at 1,000 of", results_count,"\nYelp API limits to 1,000 results per query. Consider narrowing search radius or query.")
            break
    print("\nCompleted search.")      
    print("****************************************************\n")


# Function - Check data before writing to CSV
def check_totals(query_type, query, latitude, longitude, radius):
    PARAMETERS = {query_type: query,
              'limit': 50,
              'offset': 0,
              'radius': radius,
              'latitude': latitude,
              'longitude': longitude}
    response = requests.get(url = ENDPOINT,
                        params = PARAMETERS,
                        headers = HEADERS)
    business_data = response.json()
    print("\n****************************************************")
    print("Results found for", query_type, query,":", business_data['total'], "within", radius, "meters")
    print("****************************************************\n")

def consolidated_latlong(latitude, longitude, radius):
    latlong_search("categories", "coffee", latitude, longitude, radius)
    latlong_search("categories", "cafes", latitude, longitude, radius)
    latlong_search("categories", "coffeeroasteries", latitude, longitude, radius)
    latlong_search("categories", "donuts", latitude, longitude, radius)
    latlong_search("categories", "bakeries", latitude, longitude, radius)
    latlong_search("term", "coffee", latitude, longitude, radius)
    latlong_search("term", "coffee shop", latitude, longitude, radius)
    latlong_search("term", "cafe", latitude, longitude, radius)


# Reference: Yelp supported categories can be found at 'https://www.yelp.com/developers/documentation/v3/all_category_list'

"""
# Check Totals Example - Check number of establishments within 40,000 meters (~25 miles) of New York's Time Square
check_totals("term", "coffee", 40.757958, -73.985560, 40000)
check_totals("categories", "cafes", 40.757958, -73.985560, 40000)
check_totals("categories", "coffee", 40.757958, -73.985560, 40000)
"""

"""
# Check Totals Example - Narrowing Search Radius aruond Time Square
check_totals("categories", "restaurants", 40.757958, -73.985560, 20000) # ~12 Mile Radius
check_totals("categories", "restaurants", 40.757958, -73.985560, 10000) # ~6 Mile Radius
check_totals("categories", "restaurants", 40.757958, -73.985560, 5000) # ~3 Mile Radius
check_totals("categories", "restaurants", 40.757958, -73.985560, 1000) # ~ 1/2 Mile Radius
check_totals("categories", "restaurants", 40.757958, -73.985560, 500) # ~1/4 Mile Radius
check_totals("categories", "restaurants", 40.757958, -73.985560, 100) 
"""

"""
# Multiple Search Radii - Columbus, OH
check_totals("term", "coffee", 39.935534, -82.971412, 30000) # ~ 19 Mile Radius
check_totals("term", "coffee", 39.943419, -83.121282, 35000) # ~ 22 Mile Radius
check_totals("term", "coffee", 39.985696, -82.876221, 30000) # ~ 19 Mile Radius
check_totals("term", "coffee", 40.058407, -83.024718, 35000) # ~ 22 Mile Radius
check_totals("term", "coffee", 39.894174, -82.949213, 30000) # ~ 19 Mile Radius
"""

"""
# Multiple Search Radii & Write to CSV - Columbus, OH
latlong_search("term", "coffee", 39.935534, -82.971412, 30000) # ~ 19 Mile Radius
latlong_search("term", "coffee", 39.943419, -83.121282, 35000) # ~ 22 Mile Radius
latlong_search("term", "coffee", 39.985696, -82.876221, 30000) # ~ 19 Mile Radius
latlong_search("term", "coffee", 40.058407, -83.024718, 35000) # ~ 22 Mile Radius
latlong_search("term", "coffee", 39.894174, -82.949213, 30000) # ~ 19 Mile Radius
"""

"""
# Consolidated Lat/Long Search - Multiple Criteria at Once - Columbus, OH
consolidated_latlong(39.935534, -82.971412, 30000) # ~ 19 Mile Radius
consolidated_latlong(39.943419, -83.121282, 35000) # ~ 22 Mile Radius
consolidated_latlong(39.985696, -82.876221, 30000) # ~ 19 Mile Radius
consolidated_latlong(40.058407, -83.024718, 35000) # ~ 22 Mile Radius
consolidated_latlong(39.894174, -82.949213, 30000) # ~ 19 Mile Radius
"""

print("End program.")
quit()
