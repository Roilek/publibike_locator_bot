import requests, urllib.parse

api_url = "https://api.publibike.ch/v1"
golden_bike_id = "504027"

google_api_url = "https://www.google.com/maps/search/?api=1&query="

# GET /public/partner/stations
all_partners_endpoint = "/public/partner/stations"
# GET /public/stations
all_stations = "/public/stations"
# GET /public/stations/{id}
get_station = "/public/stations/"


def query(api_endpoint):
    url = api_url + api_endpoint
    resp = requests.get(url)
    if resp.status_code == 200:
        api_data = resp.json()
    else:
        print(f"Error: {resp.status_code}")
        api_data = None
    return api_data


def locate(bike_id: str) -> str:
    # locate the golden bike
    stations_json = query(all_partners_endpoint)
    stations_array = stations_json['stations']
    found_station = None
    for s in stations_array:
        for v in s['vehicles']:
            if v['name'] == bike_id:
                found_station = s
                break

    if found_station is not None:
        print("Golden bike found!")
        print("Place: " + found_station['address'] + " in " + found_station['city'])
        query_string = found_station['address'] + " " + found_station['city']
        query_string = urllib.parse.quote(query_string)
        return google_api_url + query_string
    else:
        return "Impossible to locate the bike..."
