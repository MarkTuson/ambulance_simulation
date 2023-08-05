"""
Usage:
    analyse_individual_run.py <results>
Arguments
Arguments
    results_file : the results file to analyse
"""
import pandas as pd
import numpy as np
import tqdm
import sys


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


if __name__ == "__main__":
    args = sys.argv
    results_file = args[1]

    pecent_abandoneds = []
    mean_ambulance_utilisations = []
    mean_rrv_utilisations = []
    mean_response_times = []

    data = pd.read_csv(f"src/results/{results_file}.csv", index_col=0)
    data = data[(data["call_date"] > 25) & (data["call_date"] < 205)]
    trials = sorted(list(data["trial"].value_counts().index))

    for trial in trials:
        pecent_abandoneds.append(find_percent_abandoned(data, trial))
        mean_ambulance_utilisations.append(find_mean_ambulance_utilisation(data, trial))
        mean_rrv_utilisations.append(find_mean_rrv_utilisation(data, trial))
        mean_response_times.append(find_mean_response_time(data, trial))

    results = pd.DataFrame(
        {
            "Trial": trials,
            "Percent Abandoned": pecent_abandoneds,
            "Ambulance Utilisation": mean_ambulance_utilisations,
            "RRV Utilisation": mean_rrv_utilisations,
            "Mean Response Time": mean_response_times,
        }
    )

    results.to_csv(f"src/results/results_summary_{results_file}.csv", index=False)
