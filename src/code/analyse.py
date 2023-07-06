import pandas as pd
import numpy as np
import tqdm


def find_mean_ambulance_utilisation(data, trial):
    data_trial = data[data["trial"] == trial]
    data_nofalse = data_trial[data_trial["ambulance_id"] != "LFalse VFalse"]
    grouped_data = (
        data_nofalse.groupby(["ambulance_id", "trial"])["ambulance_service_time"]
        .sum()
        .groupby(level=0)
        .mean()
        / 93
    )
    return grouped_data.mean()


def find_mean_rrv_utilisation(data, trial):
    data_trial = data[data["trial"] == trial]
    data_nofalse = data_trial[data_trial["rrv_id"] != "LFalse VFalse"]
    grouped_data = (
        data_nofalse.groupby(["rrv_id", "trial"])["rrv_service_time"]
        .sum()
        .groupby(level=0)
        .mean()
        / 93
    )
    return grouped_data.mean()


def find_percent_abandoned(data, trial):
    data_trial = data[data["trial"] == trial]
    return (
        data_trial.isna()
        .groupby(data_trial["trial"])["ambulance_location"]
        .mean()
        .mean()
    )


def find_mean_response_time(data, trial):
    data_trial = data[data["trial"] == trial]
    data_nofalse = data_trial[data_trial["ambulance_id"] != "LFalse VFalse"]
    return data_nofalse["response_time"].mean()


def find_percent_response_time_less_than(data, trial, target):
    data_trial = data[data["trial"] == trial]
    data_nofalse = data_trial[data_trial["ambulance_id"] != "LFalse VFalse"]
    return (data_nofalse["response_time"] <= (target / (60 * 24))).mean()


def find_survival_probability(row):
    if row["speciality"] == 0:
        t = 60 * 24 * row["response_time"]
        return 1 / (1 + np.exp((0.139 * t) - 0.26))
    if row["speciality"] == 1:
        return int(row["response_time"] <= (15 / (60 * 24)))
    if row["speciality"] == 2:
        return int(row["response_time"] <= (60 / (60 * 24)))


def within_target(row):
    if row["speciality"] == 0:
        return row["response_time"] <= (8 / (60 * 24))
    if row["speciality"] == 1:
        return row["response_time"] <= (15 / (60 * 24))
    if row["speciality"] == 2:
        return row["response_time"] <= (60 / (60 * 24))


def find_percent_within_target(data, trial):
    data_trial = data[data["trial"] == trial]
    data_nofalse = data_trial[data_trial["ambulance_id"] != "LFalse VFalse"]
    return data_nofalse.apply(within_target, axis=1).mean()


def find_overall_surival(data, trial):
    data_trial = data[data["trial"] == trial]
    data_nofalse = data_trial[data_trial["ambulance_id"] != "LFalse VFalse"]
    return data_nofalse.apply(find_survival_probability, axis=1).mean()


experiments = [
    (d, s, r)
    for d in [13, 19, 34, 45]
    for s in ["noRRV", "withRRV"]
    for r in range(60, 125)
]
# experiments = ['current', 'current_61', 'allocation_best_61', 'allocation_best_81']

demand_levels = []
scenarios = []
resource_levels = []
trials = []
pecent_abandoneds = []
mean_ambulance_utilisations = []
mean_rrv_utilisations = []
mean_response_times = []
response_times_less8 = []
response_times_less15 = []
response_times_less60 = []
response_times_in_target = []
overall_survival = []

for demand, scenario, resource in tqdm.tqdm(experiments):
    # for exp in tqdm.tqdm(experiments):
    # demand=13
    # scenario='A'
    # resource='B'
    data = pd.read_csv(
        f"src/results/demand={demand}_posts=original_allocation=demand_{demand}_{scenario}_{resource}_year=2019.csv",
        index_col=0,
    )
    # data = pd.read_csv(f'src/results/demand=13_posts=original_allocation={exp}_year=2019.csv', index_col=0)
    data = data[(data["call_date"] > 6) & (data["call_date"] < 99)]
    for trial in range(12):
        demand_levels.append(demand)
        # scenarios.append(exp)
        scenarios.append(scenario)
        resource_levels.append(resource)
        trials.append(trial)
        pecent_abandoneds.append(find_percent_abandoned(data, trial))
        mean_ambulance_utilisations.append(find_mean_ambulance_utilisation(data, trial))
        mean_rrv_utilisations.append(find_mean_rrv_utilisation(data, trial))
        mean_response_times.append(find_mean_response_time(data, trial))
        response_times_less8.append(
            find_percent_response_time_less_than(data, trial, 8)
        )
        response_times_less15.append(
            find_percent_response_time_less_than(data, trial, 15)
        )
        response_times_less60.append(
            find_percent_response_time_less_than(data, trial, 60)
        )
        response_times_in_target.append(find_percent_within_target(data, trial))
        overall_survival.append(find_overall_surival(data, trial))

results = pd.DataFrame(
    {
        "Demand Level": demand_levels,
        "Scenario": scenarios,
        "Resource Level": resource_levels,
        "Trial": trials,
        "Percent Abandoned": pecent_abandoneds,
        "Ambulance Utilisation": mean_ambulance_utilisations,
        "RRV Utilisation": mean_rrv_utilisations,
        "Mean Response Time": mean_response_times,
        "Percent Response < 8": response_times_less8,
        "Percent Response < 15": response_times_less15,
        "Percent Response < 60": response_times_less60,
        "Percent Response within Target": response_times_in_target,
        "Overall Survival": overall_survival,
    }
)

results.to_csv("src/results/results_summary.csv", index=False)
