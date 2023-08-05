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
        / 180
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
        / 180
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
    for s in ["single", "multiple"]
    for r in range(60, 125, 2)
]

demand_levels = []
scenarios = []
resource_levels = []
trials = []
pecent_abandoneds = []
mean_ambulance_utilisations = []
mean_rrv_utilisations = []
mean_response_times = []

for demand, scenario, resource in tqdm.tqdm(experiments):
    data = pd.read_csv(
        f"src/results/demand={demand}_posts=original_allocation=demand_{demand}_{scenario}_{resource}_year=2019.csv",
        index_col=0,
    )
    data = data[(data["call_date"] > 25) & (data["call_date"] < 205)]
    for trial in range(12):
        demand_levels.append(demand)
        scenarios.append(scenario)
        resource_levels.append(resource)
        trials.append(trial)
        pecent_abandoneds.append(find_percent_abandoned(data, trial))
        mean_ambulance_utilisations.append(find_mean_ambulance_utilisation(data, trial))
        mean_rrv_utilisations.append(find_mean_rrv_utilisation(data, trial))
        mean_response_times.append(find_mean_response_time(data, trial))

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
    }
)

results.to_csv("src/results/results_summary.csv", index=False)
