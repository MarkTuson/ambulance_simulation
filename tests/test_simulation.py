import src.code.methods as methods

def test_convert_from_class():
    params = {
        'n_specialities': 3
    }
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
    params = {
        'n_specialities': 5
    }
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
    params = {
        'n_specialities': 3
    }
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
    params = {
        'n_specialities': 5
    }
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
	    'n_factors': 2,
	    'delay_split': [0, 0.5, 1]
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
	params = {
	    'n_factors':5,
	    'delay_split': [0, 0.2, 0.5, 0.6, 0.9, 1.0]
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


def test_find_max_dist():
	# Example where 2nd half of day is half as slow
	params = {
	    'n_factors': 2,
	    'delay_split': [0, 0.5, 1],
	    'delay_factor': [1, 0.5]
	}
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
	params = {
	    'n_factors': 2,
	    'delay_split': [0, 0.5, 1],
	    'delay_factor': [1, 2]
	}
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
	params = {
	    'n_factors': 2,
	    'delay_split': [0, 0.5, 1],
	    'delay_factor': [1, 2]
	}
	assert round(methods.final_leg(0.2, 0.1, params), 3) == 0.1
	assert round(methods.final_leg(0.2, 0.2, params), 3) == 0.2
	assert round(methods.final_leg(0.2, 0.3, params), 3) == 0.3
	assert round(methods.final_leg(0.6, 0.2, params), 3) == 0.1
	assert round(methods.final_leg(0.6, 0.4, params), 3) == 0.2
	assert round(methods.final_leg(0.6, 0.6, params), 3) == 0.3

	# Example where 2nd half of day is half as slow
	params = {
	    'n_factors': 2,
	    'delay_split': [0, 0.5, 1],
	    'delay_factor': [1, 0.5]
	}
	assert round(methods.final_leg(0.2, 0.1, params), 3) == 0.1
	assert round(methods.final_leg(0.2, 0.2, params), 3) == 0.2
	assert round(methods.final_leg(0.2, 0.3, params), 3) == 0.3
	assert round(methods.final_leg(0.6, 0.05, params), 3) == 0.1
	assert round(methods.final_leg(0.6, 0.1, params), 3) == 0.2
	assert round(methods.final_leg(0.6, 0.15, params), 3) == 0.3


def test_journey_time():
	params = {
	    'n_factors': 4,
	    'delay_split': [0/16, 4/16, 8/16, 12/16, 16/16],
	    'delay_factor': [1, 0.25, 2, 1]
	}
	# Example (a) from paper (Figure 2)
	assert methods.journey_time(0/16, 11/16, params) == 11/16
	# Breakdown
	assert methods.journey_time(0/16, 4/16, params) == 4/16
	assert methods.journey_time(0/16, 5/16, params) == 8/16
	assert methods.journey_time(0/16, 11/16, params) == 11/16

	# Example (b) from paper (Figure 2)
	assert methods.journey_time(3/16, 11/16, params) == 10/16
	# Breakdown
	assert methods.journey_time(3/16, 1/16, params) == 1/16
	assert methods.journey_time(3/16, 2/16, params) == 5/16
	assert methods.journey_time(3/16, 10/16, params) == 9/16
	assert methods.journey_time(3/16, 11/16, params) == 10/16

