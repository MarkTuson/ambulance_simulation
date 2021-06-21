This package contains the code to run an ambulance simulation. It's split into three files; data-methods creates the intial data set on which the simulation runs, methods contains the simulation methods annd main combines and runs these in the simulation itself.


# Usage

To run `5` trials or parameter set `toy_params.yml` and then write the results to `toy_results.csv`, run:

>>> python src/code/main.py src/params/toy_params.yml src/results/toy_results.csv 5