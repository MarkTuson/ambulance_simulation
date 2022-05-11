This package contains the code to run an ambulance simulation. It's split into three files; data-methods creates the intial data set on which the simulation runs, methods contains the simulation methods annd main combines and runs these in the simulation itself.


# Usage

To run `5` trials or parameter set `toy_params.yml` and then write the results to `toy_results.csv`, run:

>>> python src/code/main.py src/params/toy_params.yml src/results/toy_results.csv 5


# Parameters
## Sets
+ |H| == n_factors
+ |A| == n_ambulances
+ |P| == n_locations
+ |K| == n_specialities
+ |Y| == n_hospitals
+ H == delay_split
## Distances
+ \tilde{B}_{pa} == amb_to_patient
+ \tilde{C}_{py} == patient_to_hosp
+ \tilde{D}_{ya} == hosp_to_amb
+ \tilde{F}_{pa} == patient_to_amb
## Delay Factors
+ d_h == delay_factor
## Delay Times
+ G_k == delay_at_site
+ J_{yk} == delay_at_hosp
## Rates
+ \lambda_{pk} == loc_arrival_rates
+ s == speed
## Probabilities
+ q_{pky} == prob_hosp