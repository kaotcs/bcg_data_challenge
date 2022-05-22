##############################
####### INITIAL CONFIG #######
##############################

# import required library to configure module
from bcg_challenge.initial_config import initial_settings

# set the basic cofiguration for this module
initial_settings()

################################
####### MODULE FUNCTIONS #######
################################


def discretize_into_quantile_labales( pandas_series, num_bins = 20, bin_label_add = ''):
    """Take a pandas series and creates a label for its values based on their quantile range.

    Args
        pandas_series: a pandas series object whose values we want to discretize based on quantiles
        num_bins: an integer to define number of bins to split the column into quantiles
        bin_label_add: a string with additional information on bin labels

    Return
        discretized_series: a pandas series object with the discretization labels.
    """

    # import required libraries
    import pandas as pd

    # input verification
    assert isinstance(pandas_series, pd.core.series.Series), "Until now, this function only accepts pandas_series params as a pandas.core.series.Series! Check input type!"
    assert isinstance(num_bins, int), "num_bins param must be an integer!"
    assert isinstance(bin_label_add, str), "bin_label_add must be a string!"
    
    # define quantile values as integers -> 20, 30, 70
    quantiles = [*range(0, 100, int(100/num_bins))]
    # define quantile labels regarding quantiles values
    quantile_labels = [f"<{bin_label_add}-quantiles>{i}-{i+int(100/num_bins)}<>" for i in quantiles]
    # break the given array into "num_bins" bins taking into account quantiles
    # and label bins according to their quantile range
    discretized_series = pd.qcut(x = pandas_series,
                                 q = 20, 
                                 labels = quantile_labels)

    
    return discretized_series

