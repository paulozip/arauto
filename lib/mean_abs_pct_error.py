import numpy as np

def mean_abs_pct_error(actual_values, forecast_values):
    '''
    MAPE function to understand the average error percentage of the model

    Args.:
        actual_values (Numpy 1D Array, List or Iterable): True values of the set
        forecast_values (Numpy 1D Array, List or Iterable): Values predicted by the model
    Return:
        MAPE value (float)
    '''
    err=0
    for i in range(len(forecast_values)):
        err += np.abs(actual_values.values[i] - forecast_values.values[i]) / actual_values.values[i]
    return err * 100/len(forecast_values)