"""
Usage:
    create_params.py <data_folder> <params_name>
Arguments
    data_folder   : name of the folder where the data is kept
    params_name   : name of the parameter yml file to write
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
    data_folder = args[1]
    params_name = args[2]

    ## Travel Times
    travel_times = np.genfromtxt('src/data/global/traveltime_matrix.csv', delimiter=',')
    # Set travel time within same neighbourhood to minimum of travel time from that neighbourhood to any other neighbourhood
    temp_max = int(travel_times.max() * 2)
    num_neighbourhoods = len(travel_times)
    travel_times = travel_times + (np.eye(num_neighbourhoods) * temp_max)
    to_same_neighbouthood = travel_times.min(axis=1)
    travel_times = travel_times - (np.eye(num_neighbourhoods) * temp_max)
    travel_times = travel_times + (np.eye(num_neighbourhoods) * to_same_neighbouthood)
    travel_times = travel_times / 1440

    # mapping from ambulance index to neighbourhood index
    ambulance_neighbourhood = pd.read_csv(data_folder + 'ambulance_neigbourhood.csv', index_col='Post Serial')

    # arrival rates for each neighbourhood, accroding to speciality A1, A2, B
    demand = pd.read_csv(data_folder + 'Demand.csv', index_col='Serial_no')

    # Get destination probabilities
    destination_numbers_A1 = np.genfromtxt(data_folder + 'destination_probability_A1.csv', delimiter=',')
    destination_probabilities_A1  = np.vstack([get_row_probs(destination_numbers_A1[i]) for i in range(num_neighbourhoods)])
    destination_numbers_A2 = np.genfromtxt(data_folder + 'destination_probability_A2.csv', delimiter=',')
    destination_probabilities_A2  = np.vstack([get_row_probs(destination_numbers_A2[i]) for i in range(num_neighbourhoods)])
    destination_numbers_B = np.genfromtxt(data_folder + 'destination_probability_B.csv', delimiter=',')
    destination_probabilities_B  = np.vstack([get_row_probs(destination_numbers_B[i]) for i in range(num_neighbourhoods)])

    # Get allocation
    allocation = np.genfromtxt(data_folder + 'allocation.csv', delimiter=',')
    allocation_secondary = np.genfromtxt(data_folder + 'allocation_secondary.csv', delimiter=',')

    # Get delay splits and factors
    delay_split = np.genfromtxt('src/data/global/delay_split.csv', delimiter=',')
    delay_split_secondary = np.genfromtxt('src/data/global/delay_split_secondary.csv', delimiter=',')
    delay_factor = np.genfromtxt('src/data/global/delay_factor.csv', delimiter=',')
    delay_factor_secondary = np.genfromtxt('src/data/global/delay_factor_secondary.csv', delimiter=',')

    # Get delays at hospital and at site
    delay_at_hosp = np.genfromtxt(data_folder + 'delay_at_hosp.csv', delimiter=',')
    delay_at_site = np.genfromtxt(data_folder + 'delay_at_site.csv', delimiter=',')


    # Assemble parameters dictionary
    params = {
        'n_ambulances': len(ambulance_neighbourhood),
        'n_factors': len(delay_factor),
        'n_factors_secondary': len(delay_factor_secondary),
        'n_locations': num_neighbourhoods,
        'n_specialities': 3,
        'n_hospitals': num_neighbourhoods,
        'amb_to_patient': travel_times[ambulance_neighbourhood['Neighbourhood serial'].values].tolist(),
        'patient_to_hosp': travel_times.tolist(),
        'hosp_to_amb': travel_times.T[ambulance_neighbourhood['Neighbourhood serial'].values].T.tolist(),
        'patient_to_amb': travel_times.T[ambulance_neighbourhood['Neighbourhood serial'].values].T.tolist(),
        'delay_factor': delay_factor.tolist(),
        'delay_factor_secondary': delay_factor_secondary.tolist(),
        'delay_split': delay_split.tolist(),
        'delay_split_secondary': delay_split_secondary.tolist(),
        'delay_at_site': delay_at_site.tolist(),
        'delay_at_hosp': delay_at_hosp.tolist(),
        'loc_arrival_rates': [demand.T[i].values.tolist() for i in range(len(demand))],
        'prob_hosp': np.array([[[matrix[i, j]
            for matrix in [destination_probabilities_A1, destination_probabilities_A2, destination_probabilities_B]]
            for j in range(len(destination_probabilities_A1))]
            for i in range(len(destination_probabilities_A1))
        ]).tolist(),
        'allocation': [int(c) for c in allocation.tolist()],
        'allocation_secondary': [int(c) for c in allocation_secondary.tolist()],
    }

    # Write parameters to file
    with open(params_name, 'w') as f:
        f.write(yaml.dump(params))


