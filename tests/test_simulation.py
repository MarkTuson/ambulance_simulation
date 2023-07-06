import src.code.methods as methods
import ciw
import pandas as pd
import numpy as np


def test_convert_from_class():
    params = {"n_specialities": 3}
    assert methods.convert_from_class(0, params) == (0, 0)
    assert methods.convert_from_class(1, params) == (0, 1)
    assert methods.convert_from_class(2, params) == (0, 2)
    assert methods.convert_from_class(3, params) == (1, 0)
    assert methods.convert_from_class(4, params) == (1, 1)
    assert methods.convert_from_class(5, params) == (1, 2)
    assert methods.convert_from_class(6, params) == (2, 0)
    assert methods.convert_from_class(7, params) == (2, 1)
    assert methods.convert_from_class(8, params) == (2, 2)
    assert methods.convert_from_class(9, params) == (3, 0)
    assert methods.convert_from_class(10, params) == (3, 1)
    assert methods.convert_from_class(11, params) == (3, 2)
    params = {"n_specialities": 5}
    assert methods.convert_from_class(0, params) == (0, 0)
    assert methods.convert_from_class(1, params) == (0, 1)
    assert methods.convert_from_class(2, params) == (0, 2)
    assert methods.convert_from_class(3, params) == (0, 3)
    assert methods.convert_from_class(4, params) == (0, 4)
    assert methods.convert_from_class(5, params) == (1, 0)
    assert methods.convert_from_class(6, params) == (1, 1)
    assert methods.convert_from_class(7, params) == (1, 2)
    assert methods.convert_from_class(8, params) == (1, 3)
    assert methods.convert_from_class(9, params) == (1, 4)
    assert methods.convert_from_class(10, params) == (2, 0)
    assert methods.convert_from_class(11, params) == (2, 1)


def test_convert_to_class():
    params = {"n_specialities": 3}
    assert 0 == methods.convert_to_class(0, 0, params)
    assert 1 == methods.convert_to_class(0, 1, params)
    assert 2 == methods.convert_to_class(0, 2, params)
    assert 3 == methods.convert_to_class(1, 0, params)
    assert 4 == methods.convert_to_class(1, 1, params)
    assert 5 == methods.convert_to_class(1, 2, params)
    assert 6 == methods.convert_to_class(2, 0, params)
    assert 7 == methods.convert_to_class(2, 1, params)
    assert 8 == methods.convert_to_class(2, 2, params)
    assert 9 == methods.convert_to_class(3, 0, params)
    assert 10 == methods.convert_to_class(3, 1, params)
    assert 11 == methods.convert_to_class(3, 2, params)
    params = {"n_specialities": 5}
    assert 0 == methods.convert_to_class(0, 0, params)
    assert 1 == methods.convert_to_class(0, 1, params)
    assert 2 == methods.convert_to_class(0, 2, params)
    assert 3 == methods.convert_to_class(0, 3, params)
    assert 4 == methods.convert_to_class(0, 4, params)
    assert 5 == methods.convert_to_class(1, 0, params)
    assert 6 == methods.convert_to_class(1, 1, params)
    assert 7 == methods.convert_to_class(1, 2, params)
    assert 8 == methods.convert_to_class(1, 3, params)
    assert 9 == methods.convert_to_class(1, 4, params)
    assert 10 == methods.convert_to_class(2, 0, params)
    assert 11 == methods.convert_to_class(2, 1, params)


def test_get_delay_period():
    params = {
        "n_factors": 2,
        "n_factors_secondary": 3,
        "delay_split": [0, 0.5, 1],
        "delay_split_secondary": [0, 0.25, 0.75, 1],
    }
    assert methods.get_delay_period(0.0, params) == 0
    assert methods.get_delay_period(0.1, params) == 0
    assert methods.get_delay_period(0.2, params) == 0
    assert methods.get_delay_period(0.3, params) == 0
    assert methods.get_delay_period(0.4, params) == 0
    assert methods.get_delay_period(0.5, params) == 1
    assert methods.get_delay_period(0.6, params) == 1
    assert methods.get_delay_period(0.7, params) == 1
    assert methods.get_delay_period(0.8, params) == 1
    assert methods.get_delay_period(0.9, params) == 1
    assert methods.get_delay_period(0.0, params, secondary=True) == 0
    assert methods.get_delay_period(0.1, params, secondary=True) == 0
    assert methods.get_delay_period(0.2, params, secondary=True) == 0
    assert methods.get_delay_period(0.3, params, secondary=True) == 1
    assert methods.get_delay_period(0.4, params, secondary=True) == 1
    assert methods.get_delay_period(0.5, params, secondary=True) == 1
    assert methods.get_delay_period(0.6, params, secondary=True) == 1
    assert methods.get_delay_period(0.7, params, secondary=True) == 1
    assert methods.get_delay_period(0.8, params, secondary=True) == 2
    assert methods.get_delay_period(0.9, params, secondary=True) == 2
    params = {
        "n_factors": 5,
        "n_factors_secondary": 4,
        "delay_split": [0, 0.2, 0.5, 0.6, 0.9, 1.0],
        "delay_split_secondary": [0, 0.3, 0.6, 0.8, 1.0],
    }
    assert methods.get_delay_period(0.0, params) == 0
    assert methods.get_delay_period(0.1, params) == 0
    assert methods.get_delay_period(0.2, params) == 1
    assert methods.get_delay_period(0.3, params) == 1
    assert methods.get_delay_period(0.4, params) == 1
    assert methods.get_delay_period(0.5, params) == 2
    assert methods.get_delay_period(0.6, params) == 3
    assert methods.get_delay_period(0.7, params) == 3
    assert methods.get_delay_period(0.8, params) == 3
    assert methods.get_delay_period(0.9, params) == 4
    assert methods.get_delay_period(0.0, params, secondary=True) == 0
    assert methods.get_delay_period(0.1, params, secondary=True) == 0
    assert methods.get_delay_period(0.2, params, secondary=True) == 0
    assert methods.get_delay_period(0.3, params, secondary=True) == 1
    assert methods.get_delay_period(0.4, params, secondary=True) == 1
    assert methods.get_delay_period(0.5, params, secondary=True) == 1
    assert methods.get_delay_period(0.6, params, secondary=True) == 2
    assert methods.get_delay_period(0.7, params, secondary=True) == 2
    assert methods.get_delay_period(0.8, params, secondary=True) == 3
    assert methods.get_delay_period(0.9, params, secondary=True) == 3


def test_find_max_dist():
    # Example where 2nd half of day is half as slow
    params = {"n_factors": 2, "delay_split": [0, 0.5, 1], "delay_factor": [1, 0.5]}
    assert [round(n, 3) for n in methods.find_max_dist(0.0, params)] == [0.5, 0.5]
    assert [round(n, 3) for n in methods.find_max_dist(0.1, params)] == [0.4, 0.4]
    assert [round(n, 3) for n in methods.find_max_dist(0.2, params)] == [0.3, 0.3]
    assert [round(n, 3) for n in methods.find_max_dist(0.3, params)] == [0.2, 0.2]
    assert [round(n, 3) for n in methods.find_max_dist(0.4, params)] == [0.1, 0.1]
    assert [round(n, 3) for n in methods.find_max_dist(0.5, params)] == [0.25, 0.5]
    assert [round(n, 3) for n in methods.find_max_dist(0.6, params)] == [0.2, 0.4]
    assert [round(n, 3) for n in methods.find_max_dist(0.7, params)] == [0.15, 0.3]
    assert [round(n, 3) for n in methods.find_max_dist(0.8, params)] == [0.1, 0.2]
    assert [round(n, 3) for n in methods.find_max_dist(0.9, params)] == [0.05, 0.1]

    # Example where 2nd half of day is twice as fast
    params = {"n_factors": 2, "delay_split": [0, 0.5, 1], "delay_factor": [1, 2]}
    assert [round(n, 3) for n in methods.find_max_dist(0.0, params)] == [0.5, 0.5]
    assert [round(n, 3) for n in methods.find_max_dist(0.1, params)] == [0.4, 0.4]
    assert [round(n, 3) for n in methods.find_max_dist(0.2, params)] == [0.3, 0.3]
    assert [round(n, 3) for n in methods.find_max_dist(0.3, params)] == [0.2, 0.2]
    assert [round(n, 3) for n in methods.find_max_dist(0.4, params)] == [0.1, 0.1]
    assert [round(n, 3) for n in methods.find_max_dist(0.5, params)] == [1.0, 0.5]
    assert [round(n, 3) for n in methods.find_max_dist(0.6, params)] == [0.8, 0.4]
    assert [round(n, 3) for n in methods.find_max_dist(0.7, params)] == [0.6, 0.3]
    assert [round(n, 3) for n in methods.find_max_dist(0.8, params)] == [0.4, 0.2]
    assert [round(n, 3) for n in methods.find_max_dist(0.9, params)] == [0.2, 0.1]


def test_final_leg():
    # Example where 2nd half of day is twice as fast
    params = {"n_factors": 2, "delay_split": [0, 0.5, 1], "delay_factor": [1, 2]}
    assert round(methods.final_leg(0.2, 0.1, params), 3) == 0.1
    assert round(methods.final_leg(0.2, 0.2, params), 3) == 0.2
    assert round(methods.final_leg(0.2, 0.3, params), 3) == 0.3
    assert round(methods.final_leg(0.6, 0.2, params), 3) == 0.1
    assert round(methods.final_leg(0.6, 0.4, params), 3) == 0.2
    assert round(methods.final_leg(0.6, 0.6, params), 3) == 0.3

    # Example where 2nd half of day is half as slow
    params = {"n_factors": 2, "delay_split": [0, 0.5, 1], "delay_factor": [1, 0.5]}
    assert round(methods.final_leg(0.2, 0.1, params), 3) == 0.1
    assert round(methods.final_leg(0.2, 0.2, params), 3) == 0.2
    assert round(methods.final_leg(0.2, 0.3, params), 3) == 0.3
    assert round(methods.final_leg(0.6, 0.05, params), 3) == 0.1
    assert round(methods.final_leg(0.6, 0.1, params), 3) == 0.2
    assert round(methods.final_leg(0.6, 0.15, params), 3) == 0.3


def test_journey_time():
    params = {
        "n_factors": 4,
        "delay_split": [0 / 16, 4 / 16, 8 / 16, 12 / 16, 16 / 16],
        "delay_factor": [1, 0.25, 2, 1],
    }
    # Example (a) from paper (Figure 2)
    assert methods.journey_time(0 / 16, 11 / 16, params) == 11 / 16
    # Breakdown
    assert methods.journey_time(0 / 16, 4 / 16, params) == 4 / 16
    assert methods.journey_time(0 / 16, 5 / 16, params) == 8 / 16
    assert methods.journey_time(0 / 16, 11 / 16, params) == 11 / 16

    # Example (b) from paper (Figure 2)
    assert methods.journey_time(3 / 16, 11 / 16, params) == 10 / 16
    # Breakdown
    assert methods.journey_time(3 / 16, 1 / 16, params) == 1 / 16
    assert methods.journey_time(3 / 16, 2 / 16, params) == 5 / 16
    assert methods.journey_time(3 / 16, 10 / 16, params) == 9 / 16
    assert methods.journey_time(3 / 16, 11 / 16, params) == 10 / 16


def test_expected_pickup():
    params = {
        "n_factors": 3,
        "delay_split": [0, 0.3, 0.6, 1],
        "delay_factor": [1, 0.5, 2],
        "amb_to_patient": [[0, 0.2], [0.1, 0.1]],
    }
    # Callout in first period (no delay)
    assert (
        methods.expected_pickup(initial_call_time=0, a=0, p=0, params=params) == 0 + 0
    )
    assert (
        methods.expected_pickup(initial_call_time=0, a=1, p=0, params=params) == 0 + 0.1
    )
    assert (
        methods.expected_pickup(initial_call_time=0, a=0, p=1, params=params) == 0 + 0.2
    )
    assert (
        methods.expected_pickup(initial_call_time=0, a=1, p=1, params=params) == 0 + 0.1
    )
    # Callout in second period (half as slow)
    assert (
        methods.expected_pickup(initial_call_time=0.35, a=0, p=0, params=params)
        == 0.35 + 0
    )
    assert (
        methods.expected_pickup(initial_call_time=0.35, a=1, p=0, params=params)
        == 0.35 + 0.2
    )
    assert (
        methods.expected_pickup(initial_call_time=0.35, a=0, p=1, params=params)
        == 0.35 + 0.25 + 0.0375
    )  # start time + time in slow period + rest of time in fast period
    assert (
        methods.expected_pickup(initial_call_time=0.35, a=1, p=1, params=params)
        == 0.35 + 0.2
    )
    # Callout in third period (twice as fact)
    assert (
        methods.expected_pickup(initial_call_time=0.65, a=0, p=0, params=params)
        == 0.65 + 0
    )
    assert (
        methods.expected_pickup(initial_call_time=0.65, a=1, p=0, params=params)
        == 0.65 + 0.05
    )
    assert (
        methods.expected_pickup(initial_call_time=0.65, a=0, p=1, params=params)
        == 0.65 + 0.1
    )
    assert (
        methods.expected_pickup(initial_call_time=0.65, a=1, p=1, params=params)
        == 0.65 + 0.05
    )


def test_make_service_dist():
    params = {
        "n_factors": 3,
        "delay_split": [0, 0.3, 0.6, 1],
        "delay_factor": [1, 0.5, 2],
        "amb_to_patient": [[0, 0.2], [0.1, 0.1]],
    }
    Dist = methods.make_service_dist(params)
    assert str(Dist) == "Distribution"  # check it inherits from ciw.dists.Distribuions


def test_classify():
    test_recs = pd.DataFrame(
        {
            "rrv_pick_up_time": [np.nan, 50, 60, 70],
            "rrv_delay_at_site": [np.nan, 0.0, 10, 20],
            "ambulance_pick_up_time": [30, 40, 50, 80],
        }
    )
    expected_classifications = [
        "RRV not deployed",
        "RRV arrived too late",
        "RRV arrived after ambulance",
        "RRV arrived before ambulance",
    ]
    test_recs["classification"] = test_recs.apply(methods.classify, axis=1)
    obtained_classifications = list(test_recs["classification"])

    assert expected_classifications[0] == obtained_classifications[0]
    assert expected_classifications[1] == obtained_classifications[1]
    assert expected_classifications[2] == obtained_classifications[2]
    assert expected_classifications[3] == obtained_classifications[3]
