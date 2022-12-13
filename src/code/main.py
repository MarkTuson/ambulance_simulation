"""
Usage:
    main.py <demand> <posts> <allocation> <year> <max_time> <n_trials>
Arguments
Arguments
    demand     : the demand level: 13, 19, 34, 45
    posts      : which ambulance posts to use (original, grid_3km, grid_5km, grid_sqrt5km)
    allocation : the name of the allocation allocation
    year       : the traffic delay year: 2019, 2022
    max_time   : the maximum simulation time in days
    n_trials   : the number of trials to run
"""
import methods
import yaml
import pandas as pd
import sys

if __name__ == "__main__":
    args = sys.argv
    demand = args[1]
    posts = args[2]
    allocation = args[3]
    year = args[4]
    max_time = args[5]
    n_trials = args[6]

    params_name = f"src/params/demand={demand}_posts={posts}_allocation={allocation}_year={year}.yml"
    results_name = f"src/results/demand={demand}_posts={posts}_allocation={allocation}_year={year}.csv"
    
    with open(params_name, "r") as f:
        params = yaml.load(f, Loader=yaml.CLoader)

    all_recs = []
    for trial in range(int(n_trials)):
        recs = methods.run_full_simulation(params, float(max_time), trial)
        # print(f'Completed Trial {trial}')
        all_recs.append(recs)

    data = pd.concat(all_recs)
    data = data[data['destination'] == -1]
    data.to_csv(results_name)
