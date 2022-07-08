"""
Usage:
    main.py <params_name> <results_name> <n_trials>
Arguments
    params_name   : name of the parameter yml file
    results_name  : name of the results file to write
    n_trials      : number of trials to run
"""
import sys
from methods import *
import ciw
import yaml
import pandas as pd
import numpy as np

if __name__ == "__main__":
    args = sys.argv
    params_name = args[1]
    results_name = args[2]
    n_trials = int(args[3])

    with open(params_name, "r") as f:
        params = yaml.load(f, Loader=yaml.CLoader)

    all_recs = []
    for trial in range(n_trials):
        ciw.seed(trial)
        N_transit = create_transit_network(params)
        Q_transit = TransitSimulation(
            N_transit, node_class=TransitNode, individual_class=TransitJob, params=params
        )
        Q_transit.simulate_until_max_time(31, progress_bar=True)
        recs_transit = pd.DataFrame(Q_transit.get_all_records())
        recs_transit = recs_transit[recs_transit['destination'] == -1]
        
        initial_recs = recs_transit[recs_transit['ambulance_location'] != 'False'].sort_values('call_date').reset_index()
        N_response = create_response_network(params, initial_recs)
        Q_response = ResponseSimulation(
            N_response,
            arrival_node_class=ResponseArrivalNode,
            individual_class=ResponseJob,
            node_class=ResponseNode,
            params=params,
            initial_recs=initial_recs
        )
        Q_response.simulate_until_max_time(31, progress_bar=True)
        recs_response = Q_response.get_all_records()
        recs_response = pd.DataFrame(recs_response)
        recs_response = recs_response[recs_response['rrv_location'] != -1]
        
        recs_response = recs_response.set_index('id_number')
        recs_transit = recs_transit.set_index('id_number')
        recs = pd.concat([recs_transit, recs_response], axis=1)
        recs.replace(to_replace=False, value=np.NAN, inplace=True, method=None)
        recs['response_time'] = recs[['ambulance_pick_up_time', 'rrv_pick_up_time']].min(axis=1)
        recs['rrv_action'] = recs.apply(classify, axis=1)
        recs["Trial"] = trial
        all_recs.append(recs)

    data = pd.concat(all_recs)
    data = data[data['destination'] == -1]
    data.to_csv(results_name)
