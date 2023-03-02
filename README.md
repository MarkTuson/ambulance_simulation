This package contains the code to run an ambulance simulation. It's split into three files; data-methods creates the intial data set on which the simulation runs, methods contains the simulation methods and main combines and runs these in the simulation itself.

An example jupyter notebook of results analysis is given in `analysis.ipynb`.


# Usage

### Creating Parameter Files

To create a parameter file called for a specific scenario, run:

>>> python src/code/create_params.py <demand> <posts> <allocation> <year>

Where:
  + `<demand>` is from [`demand_13`, `demand_19`, `demand_34`, `demand_45`]
  + `<posts>` is from [`original`, `grid_3km`, `grid_5km`]
  + `<allocation>` is a name of an allocation in `src/data/posts/allocations/`
  + `<year>` is from [`2019`, `2022`]

This creates the following parameter file in `src/params/`:

`demand={<demand>}_posts={<posts>}_allocation={<allocation>}_year={<year>}.yml`


### Running the Simulation

Once a parameter file is created, to run the simulation run:

>>> src/code/main.py <demand> <posts> <allocation> <year> <max_time> <n_trials>

Where:
  + `<demand>`, `<posts>`, `<allocation>`, `<year>` is as above
  + `<max_time>` is the maximum time to run the simulation in days
  + `<n_trials>` is the number of trials of the simulation to run

This creates the following results file in `src/results/`:

`demand={<demand>}_posts={<posts>}_allocation={<allocation>}_year={<year>}.csv`

Note that the simulation starting point, date 0, is considered to be Monday 3am in the morning.


### Analysing the Results

The results are analysed by running `scr/code/analyse.py`, which writes the following file: `'src/results/results_summary.csv'`.




# Parameters

+ All global data is stored in `src/data/global/`. This includes:
    - `delay_at_hosp` the times spent at the hosptial before returning
    - `delay_at_site` the times spent at site with the patient
    - `demand_split` the times of the day where demand levels change
    - `delay_split` the times of the day where traffic levels change for primary vehicles
    - `delay_split_secondary` the times of the day where traffic levels change for secondary vehicles
    - `2019/delay_factor` the speed delay factors by which to slow down primary vehicles due to traffic
    - `2019/delay_factor_secondary` the speed delay factors by which to slow down secondary vehicles due to traffic
    - `refill.csv` the time it takes to refill vehicles
    - `destination_probability_A1.csv` the probabilities of A1 patients going to each destination from each pickup point
    - `destination_probability_A2.csv` the probabilities of A2 patients going to each destination from each pickup point
    - `destination_probability_B.csv` the probabilities of B patients going to each destination from each pickup point
    - `neighbouthood_to_neighbourhood` the traffic-free travel times between each neighbourhood in Jakarta
+ All demand data is stored in `src/data/<demand_scenario>/` (where `<demand_scenario>` can either be `demand_13`, `demand_19`, `demand_34`, or `demand_45`). These include:
    - `A1_demand` the demand of A1 patients at each neighbourhood
    - `A2_demand` the demand of A2 patients at each neighbourhood
    - `B_demand` the demand of B patients at each neighbourhood
+ All parameters specific to sets of ambulance posts are given in `src/data/posts/` under the folder corresponding to the ambulance posts name (`original/`, `grid_3km`, and `grid_5km`). This includes:
    - `ambulance_list` the order, longitudes and latitudes of the ambulance posts, including optional post names
    - `amb_to_neighbourhood` the traffic-free travel times between the ambulance posts and the neihgbourhoods
    - `neighbourhood_to_amb` the traffic-free travel times between the neighbourhoods and the ambulance posts
    - Allocations for primary vehicles are stored in `src/data/posts/allocations/`
    - Allocations for secondary vehicles are stored in `src/data/posts/allocations_secondary/` (with names identical to the corresponding primary vehicle allocation in `src/data/posts/allocations/`)
