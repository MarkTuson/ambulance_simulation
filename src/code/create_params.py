"""
Usage:
    create_params.py <data_folder> <params_name>
Arguments
    demand    : the demand level: 13, 19, 34, 45
    scenario  : the optimisation scenario: A1, A1A2
    resource  : the resource level: 75 to 99
    year      : the traffic delay year: 2019, 2022
"""

import sys
import pandas as pd
import numpy as np
import yaml

def get_row_probs(row):
    a = row
    b = row.sum()
    return np.divide(a, b, out=np.zeros_like(a), where=b!=0)


if __name__ == "__main__":
    args = sys.argv
    demand = args[1]
    scenario = args[2]
    resource = args[3]
    year = args[4]

    ## Travel Times
    travel_times = np.genfromtxt('src/data/global/traveltime_matrix.csv', delimiter=',')
    # Set travel time within same neighbourhood to minimum of travel time from that neighbourhood to any other neighbourhood
    temp_max = int(travel_times.max() * 2)
    num_neighbourhoods = len(travel_times)
    travel_times = travel_times + (np.eye(num_neighbourhoods) * temp_max)
    to_same_neighbouthood = travel_times.min(axis=1)
    travel_times = travel_times - (np.eye(num_neighbourhoods) * temp_max)
    travel_times = travel_times + (np.eye(num_neighbourhoods) * to_same_neighbouthood)
    travel_times += 5 ## To account for travel within a neighbourhood
    travel_times = travel_times / 1440

    # mapping from ambulance index to neighbourhood index
    ambulance_neighbourhood = np.genfromtxt(f'src/data/global/ambulance_order.csv', delimiter=',')
    ambulance_neighbourhood = [int(n) for n in ambulance_neighbourhood]

    # arrival rates for each neighbourhood, accroding to speciality A1, A2, B
    full_demand = pd.read_csv(f'src/data/demand_{demand}/demand.csv')

    # Get destination probabilities
    destination_numbers_A1 = np.genfromtxt(f'src/data/global/destination_probability_A1.csv', delimiter=',')
    destination_probabilities_A1  = np.vstack([get_row_probs(destination_numbers_A1[i]) for i in range(num_neighbourhoods)])
    destination_numbers_A2 = np.genfromtxt(f'src/data/global/destination_probability_A2.csv', delimiter=',')
    destination_probabilities_A2  = np.vstack([get_row_probs(destination_numbers_A2[i]) for i in range(num_neighbourhoods)])
    destination_numbers_B = np.genfromtxt(f'src/data/global/destination_probability_B.csv', delimiter=',')
    destination_probabilities_B  = np.vstack([get_row_probs(destination_numbers_B[i]) for i in range(num_neighbourhoods)])

    # Get allocation
    allocation = np.genfromtxt(f'src/data/demand_{demand}/allocations/allocation_{scenario}_{resource}.csv', delimiter=',')
    allocation_secondary = np.genfromtxt(f'src/data/demand_{demand}/allocations_secondary/allocation_{scenario}_{resource}.csv', delimiter=',')

    # Get delay splits and factors
    delay_split = np.genfromtxt('src/data/global/delay_split.csv', delimiter=',')
    delay_split_secondary = np.genfromtxt('src/data/global/delay_split_secondary.csv', delimiter=',')
    delay_factor = np.genfromtxt(f'src/data/global/{year}/delay_factor.csv', delimiter=',')
    delay_factor_secondary = np.genfromtxt(f'src/data/global/{year}/delay_factor_secondary.csv', delimiter=',')

    # Get delays at hospital and at site
    delay_at_hosp = np.genfromtxt(f'src/data/global/delay_at_hosp.csv', delimiter=',') / 1440
    delay_at_site = np.genfromtxt(f'src/data/global/delay_at_site.csv', delimiter=',') / 1440

    # Get refill time
    refill_time = np.genfromtxt(f'src/data/global/refill.csv', delimiter=',')
    refill_time = refill_time / 1440


    # Assemble parameters dictionary
    params = {
        'n_ambulances': len(ambulance_neighbourhood),
        'n_factors': len(delay_factor),
        'n_factors_secondary': len(delay_factor_secondary),
        'n_locations': num_neighbourhoods,
        'n_specialities': 3,
        'n_hospitals': num_neighbourhoods,
        'amb_to_patient': travel_times[ambulance_neighbourhood].tolist(),
        'patient_to_hosp': travel_times.tolist(),
        'hosp_to_amb': travel_times.T[ambulance_neighbourhood].T.tolist(),
        'patient_to_amb': travel_times.T[ambulance_neighbourhood].T.tolist(),
        'delay_factor': delay_factor.tolist(),
        'delay_factor_secondary': delay_factor_secondary.tolist(),
        'delay_split': delay_split.tolist(),
        'delay_split_secondary': delay_split_secondary.tolist(),
        'delay_at_site': delay_at_site.tolist(),
        'delay_at_hosp': delay_at_hosp.tolist(),
        'loc_arrival_rates': [full_demand.T[i].values.tolist() for i in range(len(full_demand))],
        'prob_hosp': np.array([[[matrix[i, j]
            for matrix in [destination_probabilities_A1, destination_probabilities_A2, destination_probabilities_B]]
            for j in range(len(destination_probabilities_A1))]
            for i in range(len(destination_probabilities_A1))
        ]).tolist(),
        'allocation': [int(c) for c in allocation.tolist()],
        'allocation_secondary': [int(c) for c in allocation_secondary.tolist()],
        'refill_time': refill_time.tolist()
    }

    # Write parameters to file
    params_name = f"src/params/demand={demand}_scenario={scenario}_resource={resource}_year={year}.yml"
    with open(params_name, 'w') as f:
        f.write(yaml.dump(params))


