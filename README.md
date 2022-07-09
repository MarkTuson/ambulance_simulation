This package contains the code to run an ambulance simulation. It's split into three files; data-methods creates the intial data set on which the simulation runs, methods contains the simulation methods and main combines and runs these in the simulation itself.

An example jupyter notebook of results analysis is given in `analysis.ipynb`.


# Usage

To create a parameter file called `src/params/base.yml` from data in the folder `src/data/base`, run:

>>> python src/code/create_params.py src/data/base/ src/params/base.yml

To run `10` trials of a simulation over `31` days, for parameter set `src/params/base.yml` and then write the results to `src/results/base.csv`, multiprocessing using `4` cores, run:

>>> python src/code/main.py src/params/base.yml src/results/tbase.csv 31 10 4


# Parameters
## Sets
+ |H| == n_factors
+ |A| == n_ambulances
+ |P| == n_locations
+ |K| == n_specialities
+ |Y| == n_hospitals
+ H == (delay_split & delay_split_secondary)
## Distances
+ \tilde{B}_{pa} == amb_to_patient
+ \tilde{C}_{py} == patient_to_hosp
+ \tilde{D}_{ya} == hosp_to_amb
+ \tilde{F}_{pa} == patient_to_amb
## Delay Factors
+ d_h == (delay_factor & delay_factor_secondary)
## Delay Times
+ G_k == delay_at_site
+ J_{yk} == delay_at_hosp
## Rates
+ \lambda_{pk} == loc_arrival_rates
## Probabilities
+ q_{pky} == prob_hosp
## Allocation
+ Z_a == allocation
+ R_a == allocation_secondary