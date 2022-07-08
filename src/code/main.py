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
        N = create_transit_network(params)
        Q = TransitSimulation(
            N, node_class=TransitNode, individual_class=TransitJob, params=params
        )
        Q.simulate_until_max_time(31, progress_bar=True)
        recs = pd.DataFrame(Q.get_all_records())
        recs["Trial"] = trial
        all_recs.append(recs)

    data = pd.concat(all_recs)
    data = data[data['destination'] == -1]
    data.to_csv(results_name)
