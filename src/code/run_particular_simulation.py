import sys
import methods
import yaml
import numpy as np


def get_survival(row):
    if row['speciality'] == 0:
        return 1 / (1 + np.exp(0.26 + (0.139 * (row['response_time'] * 1440))))
    if row['speciality'] == 1:
        return int((row['response_time'] * 1440) <= 15)
    if row['speciality'] == 2:
        return int((row['response_time'] * 1440) <= 60)

if __name__ == "__main__":
    args = sys.argv
    rl = args[1]

    with open(f'src/test_params/params_notimedependency_{rl}.yml', "r") as f:
        params = yaml.load(f, Loader=yaml.CLoader)
    
    simulation_period = 5 * 365
    warmup = 100
    cooldown = 50
    
    recs = methods.run_full_simulation(
        params=params,
        max_time=simulation_period + warmup + cooldown,
        trial=0
    )
    
    recs['survival'] = recs.apply(get_survival, axis=1)
    recs = recs[(recs['call_date'] >= warmup) & (recs['call_date'] <= warmup + simulation_period)]
    objective = recs['survival'].sum() / simulation_period
    np.savetxt(f"src/test_params/objective_{rl}.csv", [round(objective, 4)])

    temp = recs.groupby('ambulance_location')['ambulance_service_time'].sum()
    primary_utilisations = [0 if params['allocation'][a] == 0 else temp[a] / (simulation_period * params['allocation'][a]) for a in range(67)]
    np.savetxt(f"src/test_params/primary_utilisations_{rl}.csv", primary_utilisations, delimiter=',')
    
    temp = recs.groupby('rrv_location')['rrv_service_time'].sum()
    secondary_utilisations = [0 if params['allocation_secondary'][a] == 0 else temp[a] / (simulation_period * params['allocation_secondary'][a]) for a in range(67)]
    np.savetxt(f"src/test_params/secondary_utilisations_{rl}.csv", secondary_utilisations, delimiter=',')
    
    