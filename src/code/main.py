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
        N = create_ambulance_network(params)
        Q = AmbulanceSimulation(
            N, node_class=AmbulanceNode, individual_class=Patient, params=params
        )
        Q.simulate_until_max_time(100, progress_bar=True)
        recs = pd.DataFrame(Q.get_all_records())
        recs["Trial"] = trial
        all_recs.append(recs)

    pd.concat(all_recs).to_csv(results_name)
