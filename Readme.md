# Generate LAQN-BO problems
This repo provides files to generate Bayesian optimisation tasks based on LAQN data https://www.londonair.org.uk/

The code should be run in the following order:
* `python download_data.py`
* `python filter_unused_locations.py`
* `python -u get_loc_data.py`
* `python -u get_classifications.py`
* `python sort_data_years.py`
* `python generate_laqn_problems.py [year]`

The file `setup_helper.py` contains helper functions and class definitions.
`station_codes.p` contains a list of station codes which we use to download the data and auxiliary information.

The code was developed using Python 3.7.3. See `requirements.txt` for package requirements.

We recommend running the `get_[...].py` scripts with the `-u` flag.

The scripts `download_data.py`, `get_loc_data.py` and `get_classifications.py` can be slow to run.

When running `generate_laqn_problems.py`, the year to generate problems for should be given as input, e.g. `python generate_laqn_problems.py 2015`.

Once you have run the earlier scripts - including `generate_laqn_problems.py` for both 2015 and 2016 - you can run `python plot_problems.py` to reproduce the figure from the paper, and verify that the problems have been successfully generated.

The problems generated are stored as `Problem_obj`. The class has the following attributes:
* `.xx`: the features (locations) of the starting points.
* `.yy`: the labels (pollution levels) of the starting points.
* `.domain`: the features (locations) of all available points.
* `.labels`: the labels (pollution levels) of all available points.
* `.maximum`: the maximum value present among `.labels`.
* `.minimum`: the minimum value present among `.labels`.
* `.maximiser`: the features corresponding to `.maximum`.
* `.minimiser`: the features corresponding to `.minimum`.
* `.identifier`: problem identifier, of the form `[Preprocessed/Not_preprocessed]-[pollutant]-[year]-[day]`.

The objective of each problem is to find the `maximiser` using as few samples as possible. Each problem starts with 5 observed data points in `.xx` and `.yy`.
