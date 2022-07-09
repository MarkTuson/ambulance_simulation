"""
Usage:
    main.py <params_name> <results_name> <n_trials>
Arguments
    params_name   : name of the parameter yml file
    results_name  : name of the results file to write
    max_time      : maximum simulation time in days
    n_trials      : number of trials to run
    n_cores       : number of cores to run
"""
import argparse
import methods
import yaml
import pandas as pd
import multiprocessing

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('params_name', help='name of the parameter yml file')
    parser.add_argument('results_name', help='name of the results file to write')
    parser.add_argument('max_time', help='maximum simulation time in days')
    parser.add_argument('n_trials', help='number of trials to run')
    parser.add_argument('n_cores', help='number of cores to use')
    args = parser.parse_args()

    with open(args.params_name, "r") as f:
        params = yaml.load(f, Loader=yaml.CLoader)

    pool = multiprocessing.Pool(int(args.n_cores))
    arguments = [(params, float(args.max_time), trial) for trial in range(int(args.n_trials))]
    all_recs = pool.starmap(methods.run_full_simulation, arguments)

    data = pd.concat(all_recs)
    data = data[data['destination'] == -1]
    data.to_csv(args.results_name)
