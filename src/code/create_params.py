"""
Usage:
    create_params.py <demand> <posts> <allocation> <year>
Arguments
    demand     : the demand level: 13, 19, 34, 45
    posts      : which ambulance posts to use (original, grid_3km, grid_5km, grid_sqrt5km)
    allocation : the name of the allocation allocation
    year       : the traffic delay year: 2019, 2022
"""

import sys
import pandas as pd
import numpy as np
import yaml


def get_row_probs(row):
    a = row
    b = row.sum()
    return np.divide(a, b, out=np.zeros_like(a), where=b != 0)


def adjust_travel_time_matrix(matrix, const, mult):
    # fill zeroes with min
    v = matrix[matrix != 0].min()
    B = matrix + ((matrix == 0) * v)
    # add constant
    B += const
    # Divide by mult
    return B / mult


if __name__ == "__main__":
    args = sys.argv
    demand = args[1]
    posts = args[2]
    allocation = args[3]
    year = args[4]

    ## NEIGHBOURHOOD TO NEIGHBOURHOOD Travel Times
    neighbourhood_to_neighbourhood = np.genfromtxt(
        "src/data/global/neighbourhood_to_neighbourhood.csv", delimiter=","
    )
    neighbourhood_to_neighbourhood = adjust_travel_time_matrix(
        neighbourhood_to_neighbourhood, 5, 1440
    )
    num_neighbourhoods = len(neighbourhood_to_neighbourhood)

    ## NEIGHBOURHOOD TO AMBULANCE Travel Times
    neighbourhood_to_amb = np.genfromtxt(
        f"src/data/posts/{posts}/neighbourhood_to_amb.csv", delimiter=","
    )
    neighbourhood_to_amb = adjust_travel_time_matrix(neighbourhood_to_amb, 5, 1440)

    ## AMBULANCE TO NEIGHBOURHOOD Travel Times
    amb_to_neighbourhood = np.genfromtxt(
        f"src/data/posts/{posts}/amb_to_neighbourhood.csv", delimiter=","
    )
    amb_to_neighbourhood = adjust_travel_time_matrix(amb_to_neighbourhood, 5, 1440)

    # demand time of day split
    demand_split = np.genfromtxt("src/data/global/demand_split.csv", delimiter=",")

    # arrival rates for each neighbourhood, accroding to speciality A1, A2, B
    demand_A1 = pd.read_csv(
        f"src/data/demand_{demand}/A1_demand.csv",
        index_col=0,
        names=range(len(demand_split)),
    )
    demand_A2 = pd.read_csv(
        f"src/data/demand_{demand}/A2_demand.csv",
        index_col=0,
        names=range(len(demand_split)),
    )
    demand_B = pd.read_csv(
        f"src/data/demand_{demand}/B_demand.csv",
        index_col=0,
        names=range(len(demand_split)),
    )
    full_demand = [data.values.tolist() for data in [demand_A1, demand_A2, demand_B]]

    # Get destination probabilities
    destination_numbers_A1 = np.genfromtxt(
        f"src/data/global/destination_probability_A1.csv", delimiter=","
    )
    destination_probabilities_A1 = np.vstack(
        [get_row_probs(destination_numbers_A1[i]) for i in range(num_neighbourhoods)]
    )
    destination_numbers_A2 = np.genfromtxt(
        f"src/data/global/destination_probability_A2.csv", delimiter=","
    )
    destination_probabilities_A2 = np.vstack(
        [get_row_probs(destination_numbers_A2[i]) for i in range(num_neighbourhoods)]
    )
    destination_numbers_B = np.genfromtxt(
        f"src/data/global/destination_probability_B.csv", delimiter=","
    )
    destination_probabilities_B = np.vstack(
        [get_row_probs(destination_numbers_B[i]) for i in range(num_neighbourhoods)]
    )

    # Get allocation
    allocation_primary = np.genfromtxt(
        f"src/data/posts/{posts}/allocations/{allocation}.csv", delimiter=","
    )
    allocation_secondary = np.genfromtxt(
        f"src/data/posts/{posts}/allocations_secondary/{allocation}.csv", delimiter=","
    )

    # Get delay splits and factors
    delay_split = np.genfromtxt("src/data/global/delay_split.csv", delimiter=",")
    delay_split_secondary = np.genfromtxt(
        "src/data/global/delay_split_secondary.csv", delimiter=","
    )
    delay_factor = np.genfromtxt(
        f"src/data/global/{year}/delay_factor.csv", delimiter=","
    )
    delay_factor_secondary = np.genfromtxt(
        f"src/data/global/{year}/delay_factor_secondary.csv", delimiter=","
    )

    # Get delays at hospital and at site
    delay_at_hosp = (
        np.genfromtxt(f"src/data/global/delay_at_hosp.csv", delimiter=",") / 1440
    )
    delay_at_site = np.genfromtxt(f"src/data/global/delay_at_site.csv", delimiter=",")

    # Get refill time
    refill_time = np.genfromtxt(f"src/data/global/refill.csv", delimiter=",")
    refill_time = refill_time / 1440

    # Assemble parameters dictionary
    params = {
        "n_ambulances": len(allocation_primary),
        "n_factors": len(delay_factor),
        "n_factors_secondary": len(delay_factor_secondary),
        "n_locations": num_neighbourhoods,
        "n_specialities": 3,
        "n_hospitals": num_neighbourhoods,
        "amb_to_patient": amb_to_neighbourhood.tolist(),
        "patient_to_hosp": neighbourhood_to_neighbourhood.tolist(),
        "hosp_to_amb": neighbourhood_to_amb.tolist(),
        "patient_to_amb": neighbourhood_to_amb.tolist(),
        "delay_factor": delay_factor.tolist(),
        "delay_factor_secondary": delay_factor_secondary.tolist(),
        "delay_split": delay_split.tolist(),
        "delay_split_secondary": delay_split_secondary.tolist(),
        "delay_at_site": delay_at_site.tolist(),
        "delay_at_hosp": delay_at_hosp.tolist(),
        "loc_arrival_rates": full_demand,
        "demand_split": demand_split.tolist(),
        "prob_hosp": np.array(
            [
                [
                    [
                        matrix[i, j]
                        for matrix in [
                            destination_probabilities_A1,
                            destination_probabilities_A2,
                            destination_probabilities_B,
                        ]
                    ]
                    for j in range(len(destination_probabilities_A1))
                ]
                for i in range(len(destination_probabilities_A1))
            ]
        ).tolist(),
        "allocation": [int(c) for c in allocation_primary.tolist()],
        "allocation_secondary": [int(c) for c in allocation_secondary.tolist()],
        "refill_time": refill_time.tolist(),
    }

    # Write parameters to file
    params_name = f"src/params/demand={demand}_posts={posts}_allocation={allocation}_year={year}.yml"
    with open(params_name, "w") as f:
        f.write(yaml.dump(params))
