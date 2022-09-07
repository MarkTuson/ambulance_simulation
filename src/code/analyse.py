import pandas as pd
import numpy as np
import tqdm

def find_mean_ambulance_utilisation(data, trial):
    data_trial = data[data['trial']==trial]
    data_nofalse = data_trial[data_trial['ambulance_id'] != 'LFalse VFalse']
    grouped_data =  data_nofalse.groupby(['ambulance_id', 'trial'])['ambulance_service_time'].sum().groupby(level=0).mean() / 93
    return grouped_data.mean()

def find_mean_rrv_utilisation(data, trial):
    data_trial = data[data['trial']==trial]
    data_nofalse = data_trial[data_trial['rrv_id'] != 'LFalse VFalse']
    grouped_data =  data_nofalse.groupby(['rrv_id', 'trial'])['rrv_service_time'].sum().groupby(level=0).mean() / 93
    return grouped_data.mean()

def find_percent_abandoned(data, trial):
    data_trial = data[data['trial']==trial]
    return data_trial.isna().groupby(data_trial['trial'])['ambulance_location'].mean().mean()

def find_mean_response_time(data, trial):
    data_trial = data[data['trial']==trial]
    data_nofalse = data_trial[data_trial['ambulance_id'] != 'LFalse VFalse']
    return data_nofalse['response_time'].mean()


experiments = [(d, s, r, y) for d in [13, 19, 34, 45] for s in ['A1A2', 'A1'] for r in range(75, 100) for y in [2019]]

demand_levels = []
scenarios = []
resource_levels = []
trials = []
pecent_abandoneds = []
mean_ambulance_utilisations = []
mean_rrv_utilisations = []
mean_response_times = []
years = []

for (demand, scenario, resource, year) in tqdm.tqdm(experiments):
    data = pd.read_csv(f'src/results/sim_results/results/demand={demand}_scenario={scenario}_resource={resource}_year={year}.csv', index_col=0)
    data = data[(data['call_date'] > 6) & (data['call_date'] < 99)]
    for trial in range(6):
        demand_levels.append(demand)
        scenarios.append(scenario)
        resource_levels.append(resource)
        years.append(year)
        trials.append(trial)
        pecent_abandoneds.append(find_percent_abandoned(data, trial))
        mean_ambulance_utilisations.append(find_mean_ambulance_utilisation(data, trial))
        mean_rrv_utilisations.append(find_mean_rrv_utilisation(data, trial))
        mean_response_times.append(find_mean_response_time(data, trial))

results = pd.DataFrame({
    'Demand Level': demand_levels,
    'Scenario': scenarios,
    'Resource Level': resource_levels,
    'Traffic Level': years,
    'Trial': trials,
    'Percent Abandoned': pecent_abandoneds,
    'Ambulance Utilisation': mean_ambulance_utilisations,
    'RRV Utilisation': mean_rrv_utilisations,
    'Mean Response Time': mean_response_times
})

results.to_csv('src/results/results_summary.csv', index=False)
