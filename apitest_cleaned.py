import requests
import googlemaps
import datetime
import json
import dateutil.parser
import pytz

stop_dict = {'The Streets at Southpoint': '4052494', 'Erwin Rd at Fulton St (VA Hospital)': '4098134', 'Campus Dr at Chapel Circle (Admissions) (12016)': '4098182', 'Science Dr at Duke Law School (12023)': '4098194', 'PPS/Science Dr (12024)': '4098198', 'GSRB Northbound (12026)': '4098206', 'Science Drive Circle (12027)': '4098210', 'Hudson Hall (12029)': '4098214', 'Research Dr at Duke Clinic (12030)': '4098218', 'Trent Dr/School of Nursing Southbound (12034)': '4098222', 'Flowers Drive Southbound (12037)': '4098226', 'Flowers Drive Northbound (12038)': '4098230', 'Parking Garage III (12044)': '4098246', 'Nanaline Duke Building (12046)': '4098254', 'Circuit Lot Westbound (12047)': '4098258', 'Circuit Lot Eastbound (12048)': '4098262', 'Yearby St at H Lot Eastbound (12049)': '4098266', 'Yearby St at Anderson St (12050)': '4098270', 'Anderson St at Mill Village (12051)': '4098274', 'Anderson St at Lewis St (12052)': '4098278', 'Erwin Square (12055)': '4098290', 'Alexander Ave at Pace St Eastbound (12056)': '4098294', 'Erwin Mill (12064)': '4098310', '705 Broad Street (12066)': '4098314', 'Circuit Dr at Towerview Rd (12067)': '4098318', 'Morreene Rd at Campus Walk Ave (12068)': '4098322', 'Dialysis (12070)': '4098326', 'Center For Living (12073)': '4098334', 'Hock Plaza (12075)': '4098338', 'Yearby at Flowers (GC/DN Eastbound) (12081)': '4098342', 'GC/DN Westbound (12082)': '4098346', 'Anderson / Campus Drive Lot (12087)': '4098362', 'Circuit Drive at Circuit Lot Extension (12092)': '4098366', 'Circuit Drive at F.E.L. Labs Building (12093)': '4098370', 'Hillsborough Rd at 15th St (12096)': '4098374', 'LaSalle St at Circuit Lot (12102)': '4098378', 'Millenium Campus Walk East (12107)': '4098386', 'Campus Walk Ave at LaSalle St (12109)': '4098390', 'Best Products Lot (12113)': '4098406', 'Science Drive at Bryan Center Garage (12123)': '4098426', 'Gross Chem / Towerview (12124)': '4098430', 'Trent Dr at Duke Hospital South (WB)': '4098454', 'Trent Dr at Parking Deck': '4098458', 'Erwin Rd at Research Dr': '4098466', 'Fulton St at Pratt St': '4098482', 'Lasalle St at Grace Healthcare': '4098490', 'Erwin Rd at Lambeth Cir': '4098502', 'Lasalle St at Bradford Ridge Apts': '4098530', "Erwin Rd at Lenox Baker Children's Hospital": '4098554', 'Flowers Dr at Duke Gardens (Northbound)': '4098558', 'Erwin Rd at LaSalle St (WB)': '4098582', 'Morreene Rd at Erwin Rd (WB)': '4098586', 'LaSalle St at Campus Walk Ave (Belmont Apts)': '4098606', 'Morreene Rd at Sherwood Dr (NB)': '4098622', 'LaSalle St at Campus Walk Dr (Holly Hill Apts)': '4098634', 'Trent Dr at Duke Hospital South (EB)': '4098650', 'LaSalle St at Hillsborough Rd (SB)': '4098658', 'Duke University Rd at Swift Ave (EB)': '4098662', 'LaSalle St at Hillsborough Rd (NB)': '4098670', 'Erwin Rd at Fulton St (Duke University Hospital)': '4098738', 'Lasalle St at Blue Crest Ln (Blue Crest Apts)': '4098762', 'Fulton St at Erwin Rd (Duke Hospital Parking Garage)': '4098786', 'LaSalle St at Duke Manor Apts (Outbound)': '4098790', 'Chapel Dr at Duke University Rd (Alumni House)': '4098814', 'Duke University Rd at Chapel Dr': '4098858', 'Trent Dr at Erwin Rd (Clipp Research Bldg)': '4098862', 'Main St at Erwin Rd': '4098866', 'Hillsborough Rd at 9th St (13003)': '4112614', 'East Campus Quad (12003)': '4117202', 'DMP/Cancer Ctr (12105)': '4128254', 'LaSalle St at Kangaroo St (The Heights Apts)': '4134094', 'Research Dr at Erwin Rd (Eye Center Garage)': '4136130', 'West Campus Chapel (12018)': '4146366', 'Smith Warehouse Westbound (12071)': '4158230', 'Duke Hospital (12114)': '4158254', 'Towerview at Circuit Dr (13005)': '4158262', 'South Square (13006)': '4173276', 'Rutherford / Main (12101)': '4174454', 'Research Dr at Circuit Dr': '4177596', 'LSRC Bld (12045)': '4186122', 'Laundry Westbound (12005)': '4188198', 'Campus Dr at Swift Ave (Westbound) (12007)': '4188200', 'Campus Dr at Swift Ave (Eastbound) (12008)': '4188202', 'Nasher  Westbound (12009)': '4188204', 'Campus Drive At Chapel Circle Eastbound (12015)': '4188206', 'Ronald Mcdonald House Eastbound (12053)': '4188210', 'Swift Avenue Eastbound (12059)': '4188214', 'Anderson St at Campus Dr (12086)': '4188216', 'Swift Ave at Faber St (13008)': '4188220', '1901 Erwin Rd (Eastbound) (13014)': '4188222', 'Campus Dr at Central Campus (Eastbound) (12010)': '4189276', 'Campus/Anderson Westbound (12011)': '4189278', 'Campus / Maxwell Westbound (12072)': '4189284', 'Circuit Dr at North Building (12103)': '4190626', 'Chapel Dr at Duke University Rd (Duke News)': '4191614', 'Oregon St at Pace St (13018)': '4192460', 'Bassett Dr at Grounds Lot (12001)': '4195800', 'Gilbert-Addoms Westbound (12002)': '4195802', 'Campus / Maxwell Eastbound (12004)': '4195804', 'Laundry Eastbound (12006)': '4195806', 'Campus/Anderson Eastbound (12012)': '4195808', 'Science Drive at Bioscience (Southbound) (12025)': '4195810', 'Fuqua School/Northbound (12060)': '4195812', 'Smith Warehouse Eastbound (12077)': '4195814', 'Rutherford / Hillsborough (12088)': '4195816', 'East Campus Statue (12130)': '4195820', 'Swift Ave at 300 Swift (13009)': '4195822', 'Swift Ave at Campus Dr (13013)': '4195824', 'Campus Dr at Nasher (Eastbound) (13015)': '4195826', 'Science Dr at Bassett Dr Northbound (13016)': '4195828', "Devil's Bistro (13300)": '4197174', 'Towerview Rd at Wannamaker (outbound) (13011)': '4198134', 'Swift Ave at Duke University Rd (13021)': '4198138', 'Imperial Building': '4198140', 'Towerview Rd at Edens B/C (14000)': '4198142', 'Towerview Rd at Wilson Gym (14001)': '4198144', 'Towerview Rd at Sanford PPS (14002)': '4198146', 'Law / Towerview (6184)': '4209466', 'Fuqua School/Southbound (6185)': '4209468', 'R. David Thomas Center (6186)': '4209470', 'Holly Ridge/Campus Walk East (5074)': '4209472', 'Safeway St at Ninth St': '4209474', 'Elf St at Elder St': '4212916', 'American Tobacco Campus': '4216582', 'Chesterfield Building': '4216584', 'Alexander Ave at Pace St Westbound': '4230936', 'The Heights at LaSalle': '4230938', 'LaSalle at Campus Walk (Southbound)': '4230940', 'Blue Crest / LaSalle South': '4230942', 'LaSalle St at Duke Manor Apts (Northbound)': '4230944'}
route_dict = {'4013334': 'C1: Express', '4003714': 'PR1: Bassett-Research', '4003718': 'H2: Hospital Loop', '4003722': 'H5: Broad-Erwin', '4003726': 'H6: Remote Lot-Hospital', '4003734': 'LL: LaSalle Loop', '4007592': 'C1: East-West Weekends', '4007670': 'H2: Tripper', '4008330': 'C1: East-West', '4008332': 'CSW: Smith Warehouse', '4008334': 'C3: East-Science', '4008336': 'CCX: Central Campus Express Weekend', '4008340': 'C3: Class Change', '4008342': 'C2 East-Central-West', '4009300': 'LL: Tripper', '4009304': 'Swift Express', '4011062': 'Shuttle: Downtown Pilot', '4013062': 'C1S'}

#yourdate = dateutil.parser.parse(datestring)
#parses ISO 8601 time into UTC time

'''
url = "https://transloc-api-1-2.p.rapidapi.com/agencies.json"

querystring = {"callback":"call"}

headers = {
    'x-rapidapi-host': "transloc-api-1-2.p.rapidapi.com",
    'x-rapidapi-key': "f551e2413fmshdf4a94f2aeeee4cp1df68djsn931c020aa943"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
### Gathering list of Routes
url = "https://transloc-api-1-2.p.rapidapi.com/routes.json"

querystring = {"callback":"call","agencies":"176"}

headers = {
    'x-rapidapi-host': "transloc-api-1-2.p.rapidapi.com",
    'x-rapidapi-key': "f551e2413fmshdf4a94f2aeeee4cp1df68djsn931c020aa943"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
'''
### Gathering List of Stops
url = "https://transloc-api-1-2.p.rapidapi.com/stops.json"

querystring = {"callback":"call","agencies":"176"}

headers = {
    'x-rapidapi-host': "transloc-api-1-2.p.rapidapi.com",
    'x-rapidapi-key': "API_KEY_HERE"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
'''
'''
'''
url = "https://transloc-api-1-2.p.rapidapi.com/routes.json"

querystring = {"callback":"call","agencies":"176"} #I believe Duke's number is 176

headers = {
    'x-rapidapi-host': "transloc-api-1-2.p.rapidapi.com",
    'x-rapidapi-key': "f551e2413fmshdf4a94f2aeeee4cp1df68djsn931c020aa943"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
parsed = response.json()
route_list = parsed["data"]["176"]
route_dict = {}
for route_info in route_list:
    route_id = route_info["route_id"]
    route_name = route_info["long_name"]
    route_dict[route_id] = route_name
print(route_dict)
'''
'''
response = requests.request("GET", url, headers=headers, params=querystring)
parsed = response.json()
stop_list = parsed["data"]
stop_dict = {}
for stop_info in stop_list:
    stop_id = stop_info["stop_id"]
    stop_name = stop_info["name"]
    stop_dict[stop_name] = stop_id
'''

gmaps = googlemaps.Client(key='API_KEY_HERE')
now = datetime.datetime.now()


def parse_directions(directions_result):
    took_bus_yet = False
    bus_segment = {"to_stop_sec": 0, "from_stop_sec": 0}
    outer_step = directions_result[0]["legs"][0]["steps"] #I parsed thru the json
    for step in outer_step:
        if step["travel_mode"] == "WALKING" and took_bus_yet == False:
            bus_segment["to_stop_sec"] += step["duration"]["value"]
        if step["travel_mode"] == "WALKING" and took_bus_yet == True:
            bus_segment["from_stop_sec"] += step["duration"]["value"]
        if step["travel_mode"] == "TRANSIT":
            bus_segment["end_coord"] = step["end_location"]
            bus_segment["start_coord"] = step["start_location"]
            bus_segment["end_stop"] = step["transit_details"]["arrival_stop"]["name"]
            bus_segment["departure_stop"] = step["transit_details"]["departure_stop"]["name"]
            took_bus_yet = True
            #bus_segment["departure_time"] = datetime.fromtimestamp(step["transit_details"]["departure_time"]["value"]).replace(tzinfo=pytz.UTC)
    bus_segment["departure_time"] = now + datetime.timedelta(seconds=bus_segment["to_stop_sec"]) #Time to get to bus stop from now
    bus_segment["initial_time"] = now
    return bus_segment

def calc_arrival_estimates(origin_id, dest_id):
    url = "https://transloc-api-1-2.p.rapidapi.com/arrival-estimates.json"
    querystring = {"stops":origin_id + "," + dest_id, "callback": "call", "agencies": "176"}
    headers = {
        'x-rapidapi-host': "transloc-api-1-2.p.rapidapi.com",
        'x-rapidapi-key': "API_KEY_HERE_3"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    return response

### Actual travel time predictor portion
now = datetime.datetime.now()
departure_loc = "Jarvis Dorm, Durham, NC"
arrival_loc = "Penn Pavilion, Durham, NC"
directions_result = gmaps.directions(departure_loc,
                                     arrival_loc,
                                     mode="transit",
                                     departure_time=now)
bus_segment = parse_directions(directions_result)
for key in stop_dict:
    if bus_segment["departure_stop"] in key:
        origin_id = stop_dict[key]
    if bus_segment["end_stop"] in key:
        dest_id = stop_dict[key]
arriv_est = calc_arrival_estimates(origin_id, dest_id)
parsed_est = arriv_est.json()
ETA_dict = {"vehicle_id": 0, "route_id":0, "route_name": "", "waiting_at_stop": 0, "departure_time": 0, "arrival_time": 0, "bus": 0}
for stop in parsed_est["data"]:
    if stop["stop_id"] == origin_id:
        for a in stop["arrivals"]:
            time = dateutil.parser.parse(a["arrival_at"]).replace(tzinfo=None)
            if time > bus_segment["departure_time"]: #the arrival time must occur after you've wwalked to bus stop
                ETA_dict["vehicle_id"] = a["vehicle_id"]
                ETA_dict["route_id"] = a["route_id"]
                ETA_dict["route_name"] = route_dict[a["route_id"]]
                ETA_dict["departure_time"] = time.replace(tzinfo=None)
                ETA_dict["waiting_at_stop"] = time - bus_segment["departure_time"]
                break
        break
#then run the whole thing over again
for stop in parsed_est["data"]:
    if stop["stop_id"] == dest_id:
        for a in stop["arrivals"]:
            time = dateutil.parser.parse(a["arrival_at"]).replace(tzinfo=None)
            vehicle = a["vehicle_id"]
            if vehicle == ETA_dict["vehicle_id"] and time > ETA_dict["departure_time"]:
                ETA_dict["arrival_time"] = time
                ETA_dict["bus"] = ETA_dict["arrival_time"] - ETA_dict["departure_time"]
                break
        break
print(ETA_dict)
only_time_moving = (datetime.timedelta(seconds = (bus_segment["to_stop_sec"] + bus_segment["from_stop_sec"]))
                    + ETA_dict["bus"]).total_seconds()
including_wait_time = (datetime.timedelta(
    seconds = (bus_segment["to_stop_sec"]
                + bus_segment["from_stop_sec"]))
              + ETA_dict["bus"] + ETA_dict["waiting_at_stop"]).total_seconds()
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











