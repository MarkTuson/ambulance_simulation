import requests
import json
import numpy as np
import pandas as pd


"""
SECTION: Records
"""


def initialise_record(column_headers):
    """
    Initialises the record keeping data structure
    STILL UNDER DEVLOPMENT

    Inputs
    ------
    column_headers - a list of strings describing each column of data
    currently these are:
        'time' - time stamp (float) for event
        'event' - a string describing the event
        'ambulance_availability' - a list of integer lists in which each        integer list describes the ambulance availability for a specific ambulance station; index[0] describes the allocation of vehicles of type 0, index[1] the number of type 0 vehicles available for service, index[2] describes the allocation of vehicles of type 1, index[3] the number of type 1 vehicles available for service, and so on..
        travel_times - a list of travel times associated with the event (if relevant), index[0] the time to travel from the station to the patient location, index[1] time on site, index[2] site to hospital, index[3] handover time, index[4] time to return from hospital to station and restock.



    outputs
    -------
    An empty panda dataframe with the columns in place

    """
    return pd.DataFrame(columns=(column_headers))


def update_record(
    record, column_headers, time, event, ambulance_availability, travel_times
):
    """
    Updates the record when called

    Inputs
    ------
    record - a panda dataframe created using the initialise_record function.
    The  should mirror the column_headers list, in both name and data type.

    Outputs
    -------
    Record dataframe with an additional row of data

    """
    event_record = pd.DataFrame(
        [[time, event, ambulance_availability, travel_times]], columns=column_headers
    )
    print(record.append(event_record, ignore_index=True))
    return record.append(event_record, ignore_index=True)


"""
SECTION: Traffic data methods 
"""


def configure_csv_data(filepath):
    """
    Takes data from a csv file and configures it into correct form for use in get_travel_times function (as trial_data).

    Inputs
    ------
    filepath - leads to csv file containg data. The file consists of three columns ('A', 'B', and 'C'), each row represents a location with column A indiciating whether it is an origin (0) or destination (1), column B the latitude and column C the longitude.

    Outputs
    -------
    json file in correct format, eg:

       {
            "origins": [
                {"point": {"latitude": 45.458545, "longitude": 9.150490}},
                ...
                {"point": {"latitude": 45.403337, "longitude": 11.050541}},
            ],
            "destinations": [
                {"point": {"latitude": 48.149853, "longitude": 11.499931}},
                ...
                {"point": {"latitude": 45.403337, "longitude": 11.050541}},
            ],
        }
    """
    data = np.genfromtxt(filepath, delimiter=",")
    location_data = {"origins": [], "destinations": []}
    for row in data:
        if row[0] == 0:
            location_data["origins"].append(
                {"point": {"latitude": row[1], "longitude": row[2]}}
            )
        else:
            location_data["destinations"].append(
                {"point": {"latitude": row[1], "longitude": row[2]}}
            )
    return location_data


def get_travel_times(apiKey, departure_time, trial_data):
    """
    Generates and sends a 'POST' to the TomTom api the data returned is used to form the travel matrix

    Inputs
    ------
    apikey - string
    departure_time - string
        Uses the "2021-01-27T22:58:00Z" format
    trial_data - JSON file
        Follows the format below:

        trial_data = {
            "origins": [
                {"point": {"latitude": 45.458545, "longitude": 9.150490}},
                ...
                {"point": {"latitude": 45.403337, "longitude": 11.050541}},
            ],
            "destinations": [
                {"point": {"latitude": 48.149853, "longitude": 11.499931}},
                ...
                {"point": {"latitude": 45.403337, "longitude": 11.050541}},
            ],
        }

    Output:
    -------
    JSON file
        The main part of the file is broken down into a 'response' for each element of the matrix, each of which describes the data relating to an origin and destination location, each 'response' contains the data below:

    {'routeSummary': {'lengthInMeters': 487625, 'travelTimeInSeconds': 17213, 'trafficDelayInSeconds': 33, 'departureTime': '2021-01-27T23:58:00+01:00', 'arrivalTime': '2021-01-28T04:44:53+01:00'}}
    """
    url = (
        "https://api.tomtom.com/routing/1/matrix/sync/json?key="
        + apiKey
        + "&departAt="
        + departure_time
        + "&routeType=fastest&travelMode=car"
    )
    response = requests.post(url, json=trial_data)
    return json.loads(response.text)


def construct_travel_matrix(info, num_origins, num_destinations):
    """
    Takes the ouput from an api request and transfomes it into a travel matrix for use in a simulation

    Inputs
    ------
    info - json file
        Of the specific format generated by the 'get_travel_times' function
    num_origins - integer
        The number of origin locations
    num_destinations - integer
        The number of destination locations

    Output:
    2d numpy array
        Rows represent origin locations, columns destination locations, the entry in each corresponds to the forecast travel time in minutes.
    """
    raw_data = []
    for i in range(num_origins):
        for j in range(num_destinations):
            raw_data.append(
                info["matrix"][i][j]["response"]["routeSummary"]["travelTimeInSeconds"]
                / 60
            )
    travel_data = np.array(raw_data)
    travel_matrix = travel_data.reshape(num_origins, num_destinations)
    return travel_matrix


def construct_preference_matrix(travel_matrix, num_origins):
    """
    Takes a travel matrix and converts it into a preference matrix using shortest travel times, for use in simulation

    Input
    -----
    2d numpy array
        Rows represent origin locations, columns destination locations, the entry in each corresponds to the forecast travel time in minutes.
    num_origins - integer
        The number of origin locations

    Output:
     2d numpy array
        Rows represent demand_node locations, columns represent order of preference, column 0 is the preferred option, followed by column 1 then 2 and so on...

    """
    g = []
    for demand_node in range(num_origins):
        z = np.copy(travel_matrix)
        a = z[demand_node]
        b = []
        for i in range(len(a)):
            b.append(np.argmin(a))
            a[np.argmin(a)] = 10000
        g.append(b)
    return np.array(g)
