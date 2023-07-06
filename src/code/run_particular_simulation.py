import sys
import methods
import yaml
import numpy as np


def get_survival(row):
    if row["speciality"] == 0:
        return 1 / (1 + np.exp(0.26 + (0.139 * (row["response_time"] * 1440))))
    if row["speciality"] == 1:
        return int((row["response_time"] * 1440) <= 15)
    if row["speciality"] == 2:
        return int((row["response_time"] * 1440) <= 60)


if __name__ == "__main__":
    with open(
        f"src/params/demand=13_posts=original_allocation=current_year=2019.yml", "r"
    ) as f:
        params = yaml.load(f, Loader=yaml.CLoader)

    simulation_period = 365
    warmup = 50
    cooldown = 10

    recs = methods.run_full_simulation(
        params=params,
        max_time=simulation_period + warmup + cooldown,
        trial=0,
        progress_bar=True,
    )

    recs["survival"] = recs.apply(get_survival, axis=1)
    recs = recs[
        (recs["call_date"] >= warmup)
        & (recs["call_date"] <= warmup + simulation_period)
    ]
    recs.to_csv("current_results.csv")
