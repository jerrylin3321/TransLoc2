import requests
import googlemaps
import datetime
import dateutil.parser

def calc_arrival_estimates(origin_id, dest_id):
    url = "https://transloc-api-1-2.p.rapidapi.com/arrival-estimates.json"
    querystring = {"stops": origin_id + "," + dest_id, "callback": "call", "agencies": "176"}
    headers = {
        'x-rapidapi-host': "transloc-api-1-2.p.rapidapi.com",
        'x-rapidapi-key': "API_KEY_HERE_3"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    return response.json()

def find_origin_and_destination_ids(bus_segment, stop_dict):
    origin_id = dest_id = None
    for key in stop_dict:
        if bus_segment["departure_stop"] in key:
            origin_id = stop_dict[key]
        if bus_segment["end_stop"] in key:
            dest_id = stop_dict[key]
    return origin_id, dest_id

def calculate_eta(parsed_est, bus_segment, route_dict, origin_id):
    ETA_dict = {"vehicle_id": 0, "route_id": 0, "route_name": "", "waiting_at_stop": 0, "departure_time": 0, "arrival_time": 0, "bus": 0}
    for stop in parsed_est["data"]:
        if stop["stop_id"] == origin_id:
            for arrival in stop["arrivals"]:
                time = dateutil.parser.parse(arrival["arrival_at"]).replace(tzinfo=None)
                if time > bus_segment["departure_time"]: # The arrival time must occur after you've walked to the bus stop
                    ETA_dict.update({
                        "vehicle_id": arrival["vehicle_id"],
                        "route_id": arrival["route_id"],
                        "route_name": route_dict[arrival["route_id"]],
                        "departure_time": time.replace(tzinfo=None),
                        "waiting_at_stop": time - bus_segment["departure_time"]
                    })
                    return ETA_dict
    return ETA_dict

def finalize_eta(parsed_est, ETA_dict, dest_id):
    for stop in parsed_est["data"]:
        if stop["stop_id"] == dest_id:
            for arrival in stop["arrivals"]:
                time = dateutil.parser.parse(arrival["arrival_at"]).replace(tzinfo=None)
                vehicle = arrival["vehicle_id"]
                if vehicle == ETA_dict["vehicle_id"] and time > ETA_dict["departure_time"]:
                    ETA_dict["arrival_time"] = time
                    ETA_dict["bus"] = ETA_dict["arrival_time"] - ETA_dict["departure_time"]
                    return
    return

# Actual travel time predictor portion
now = datetime.datetime.now()
departure_loc = "Jarvis Dorm, Durham, NC"
arrival_loc = "Penn Pavilion, Durham, NC"
directions_result = gmaps.directions(departure_loc, arrival_loc, mode="transit", departure_time=now)
bus_segment = parse_directions(directions_result) # Assuming parse_directions is defined elsewhere
origin_id, dest_id = find_origin_and_destination_ids(bus_segment, stop_dict)
parsed_est = calc_arrival_estimates(origin_id, dest_id)
ETA_dict = calculate_eta(parsed_est, bus_segment, route_dict, origin_id)
finalize_eta(parsed_est, ETA_dict, dest_id)

print("Bus route: " + ETA_dict["route_name"],
    "Only_time_moving: " + str(only_time_moving),
    "Total time including waitime: " + str(including_wait_time),
      "Time spent on bus: " + str(ETA_dict["bus"].total_seconds()),
     "Departure time: " + bus_segment["initial_time"].strftime("%Y-%m-%d %H:%M:%S"),
      "Time when you first get to bus stop:" + bus_segment["departure_time"].strftime("%Y-%m-%d %H:%M:%S"),
      "Time when you get on the bus:" + ETA_dict["departure_time"].strftime("%Y-%m-%d %H:%M:%S"),
      "Time when you get off the bus:" + ETA_dict["arrival_time"].strftime("%Y-%m-%d %H:%M:%S"),
      "Final arrival time:" + (ETA_dict["arrival_time"] + datetime.timedelta(seconds=bus_segment["from_stop_sec"])).strftime("%Y-%m-%d %H:%M:%S"),
      sep='\n')











