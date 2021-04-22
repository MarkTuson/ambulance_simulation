import json
import numpy as np
import src.code.data_methods as data_methods
import src.code.methods as methods


fname = "/Users/Mark Tuson/Dropbox/Mark/TomTom_API_key.txt"
file = open(fname, "r")
apiKey = file.read()
filepath = "tests/sample.csv"


departure_time = "2022-01-12T11:12:00Z"


trial_data = {
    "origins": [
        {"point": {"latitude": -6.2977565, "longitude": 106.7608377}},
        {"point": {"latitude": -6.1953794, "longitude": 106.8233481}},
        {"point": {"latitude": -6.20773, "longitude": 106.825748}},
    ],
    "destinations": [
        {"point": {"latitude": -6.12380601, "longitude": 106.8335255}},
        {"point": {"latitude": -6.14561972, "longitude": 106.7955737}},
        {"point": {"latitude": -6.28169312, "longitude": 106.853078}},
        {"point": {"latitude": -6.21944734, "longitude": 106.8664222}},
        {"point": {"latitude": -6.31276533, "longitude": 106.9024031}},
        {"point": {"latitude": -6.26343036, "longitude": 106.8186108}},
        {"point": {"latitude": -6.32481169, "longitude": 106.8473836}},
        {"point": {"latitude": -6.2790124, "longitude": 106.861417}},
        {"point": {"latitude": -6.20871426, "longitude": 106.8090594}},
        {"point": {"latitude": -6.23531182, "longitude": 106.8671028}},
    ],
}

test_travel_matrix = np.array([[5, 7, 3, 4], [4, 5, 8, 6], [3, 9, 4, 3]])

test_preference_matrix = np.array([[2, 3, 0, 1], [0, 1, 3, 2], [0, 3, 2, 1]])

num_origins = 3  # equivalent to number of demand nodes

num_destinations = 10

test_post_response = {
    "formatVersion": "0.0.1",
    "matrix": [
        [
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 36306,
                        "travelTimeInSeconds": 3070,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T19:03:09+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 27473,
                        "travelTimeInSeconds": 2276,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:49:56+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 15775,
                        "travelTimeInSeconds": 2247,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:49:26+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 28169,
                        "travelTimeInSeconds": 2795,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:58:34+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 18839,
                        "travelTimeInSeconds": 2069,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:46:29+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 11694,
                        "travelTimeInSeconds": 1771,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:41:31+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 17810,
                        "travelTimeInSeconds": 2486,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:53:26+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 16731,
                        "travelTimeInSeconds": 2495,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:53:35+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 15477,
                        "travelTimeInSeconds": 2072,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:46:31+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 24789,
                        "travelTimeInSeconds": 2625,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:55:45+07:00",
                    }
                },
            },
        ],
        [
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 11208,
                        "travelTimeInSeconds": 2168,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:48:08+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 9524,
                        "travelTimeInSeconds": 1671,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:39:51+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 19785,
                        "travelTimeInSeconds": 3363,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T19:08:03+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 7591,
                        "travelTimeInSeconds": 1562,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:38:01+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 20857,
                        "travelTimeInSeconds": 3011,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T19:02:11+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 9855,
                        "travelTimeInSeconds": 2084,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:46:43+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 24758,
                        "travelTimeInSeconds": 3680,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T19:13:20+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 18788,
                        "travelTimeInSeconds": 3217,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T19:05:37+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 4076,
                        "travelTimeInSeconds": 837,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:25:56+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 9505,
                        "travelTimeInSeconds": 1870,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:43:09+07:00",
                    }
                },
            },
        ],
        [
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 12745,
                        "travelTimeInSeconds": 2366,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:51:26+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 13184,
                        "travelTimeInSeconds": 1656,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:39:35+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 15249,
                        "travelTimeInSeconds": 3236,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T19:05:56+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 7499,
                        "travelTimeInSeconds": 1576,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:38:16+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 19921,
                        "travelTimeInSeconds": 2885,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T19:00:04+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 8919,
                        "travelTimeInSeconds": 1960,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:44:40+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 23822,
                        "travelTimeInSeconds": 3555,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T19:11:14+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 14252,
                        "travelTimeInSeconds": 3088,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T19:03:28+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 3837,
                        "travelTimeInSeconds": 849,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:26:09+07:00",
                    }
                },
            },
            {
                "statusCode": 200,
                "response": {
                    "routeSummary": {
                        "lengthInMeters": 9413,
                        "travelTimeInSeconds": 1884,
                        "trafficDelayInSeconds": 0,
                        "trafficLengthInMeters": 0,
                        "departureTime": "2022-01-12T18:12:00+07:00",
                        "arrivalTime": "2022-01-12T18:43:23+07:00",
                    }
                },
            },
        ],
    ],
    "summary": {"successfulRoutes": 30, "totalRoutes": 30},
}


expected_matrix = np.array(
    [
        [
            51.16666667,
            37.93333333,
            37.45,
            46.58333333,
            34.48333333,
            29.51666667,
            41.43333333,
            41.58333333,
            34.53333333,
            43.75,
        ],
        [
            36.13333333,
            27.85,
            56.05,
            26.03333333,
            50.18333333,
            34.73333333,
            61.33333333,
            53.61666667,
            13.95,
            31.16666667,
        ],
        [
            39.43333333,
            27.6,
            53.93333333,
            26.26666667,
            48.08333333,
            32.66666667,
            59.25,
            51.46666667,
            14.15,
            31.4,
        ],
    ]
)


def test_configure_csv_data():
    assert trial_data == data_methods.configure_csv_data(filepath)


"""
def test_tomtom_post():
    pass
"""


def test_construct_travel_matrix():
    assert np.allclose(
        expected_matrix,
        data_methods.construct_travel_matrix(
            test_post_response, num_origins, num_destinations
        ),
    )


def test_construct_preference_matrix():
    assert np.allclose(
        test_preference_matrix,
        data_methods.construct_preference_matrix(test_travel_matrix, num_origins),
    )
