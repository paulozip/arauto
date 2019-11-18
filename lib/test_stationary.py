import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st

from statsmodels.tsa.stattools import adfuller
from transformation_function import timeSeriesTransformer

def test_stationary(timeseries, plot_results=False, data_frequency=None, force_transformation_technique=None, custom_transformation_size=None):
    '''
    Augmented Dickey-Fuller Test in order to check if we have a stationary series

    This function will perform different transformations (log transformation, difference, seasonal difference, etc.),
    and then will apply the ADF Test. At the end of this process, this function will return (along with other things)
    the best transformed data based on the lowest significant statistical test.

    Args:
        timeseries (Pandas Series): a timeseries to be used for the statistical tests and transformations
        plot_results (bool): Wether or not to plot the best time series transformation
        data_frequency (str, optional): the frequency that the data was collected (daily, monthly, yearly, etc.)
        force_transformation_technique (str, optional): the name of a transformation technique to force. This argument 
            is passed by choosing one item from the sidebar
        custom_transformation_size (tuple of integers, optional): if a custom difference technique is selecting, we inform the amount of differences to take
            with this argument. Pass one value for difference and another for seasonal difference
        force_transformation_technique (str): a transformation technique name to be forced on this function
        custom_transformation_size (tuple of integers): a 2-sized tuple containing a integer for the differencing terms, 
            and one for seasonal differencing terms
    
    Return:
        original_timeseries (Pandas Series): the original time series passed to the function 
        d (int): suggested value to be used for d (i) terms 
        D (int): suggested value to be used for D (seasonal difference) terms 
        seasonality (int): the seasonal frequency that occurs in the time series. It's based on the data_frequency parameter
        timeseries (Pandas Series): a transformed time series based on the best stationarity transformation (differencing, log, etc.)
        transformation_function (function): the function that was used to transform the time series to be stationary. 
        It can be a lambda function or a Numpy Log function (np.log1p)
    '''
    
    transformer = timeSeriesTransformer(timeseries, data_frequency)
    progress_bar = st.progress(0)

    if force_transformation_technique != None and force_transformation_technique != 'Choose the best one':
        if force_transformation_technique == 'No transformation':
            best_transformation = transformer.test_absolute_data()
        if force_transformation_technique == 'First Difference':
            best_transformation = transformer.test_first_difference()
        if force_transformation_technique == 'Log First Difference':
            best_transformation = transformer.test_log_difference()
        if force_transformation_technique == 'Log transformation':
            best_transformation = transformer.test_log_transformation()
        if force_transformation_technique == 'Seasonal Difference':
            best_transformation = transformer.test_seasonal_difference()
        if force_transformation_technique == 'Log Difference + Seasonal Difference':
            best_transformation = transformer.test_seasonal_log_difference()
        if force_transformation_technique == 'Custom Difference':
            # If a null value is passed by custom_transformation_size argument, raise an error
            if custom_transformation_size == None:
                raise ValueError('You cannot pass a empty value for Difference size and Seasonal Difference size')
            # Executing test for custom difference
            best_transformation = transformer.test_custom_difference(custom_transformation_size)

        # If the test is not statistically significant, raise a Warning
        if best_transformation[2] == None:
            warn_message = '''
                            This custom transformation is not statistically significant. 
                            The Adfuller test result in {:.3f}, and the critical value of 1% is {:.3f}
                            '''.format(best_transformation[0][0], best_transformation[0][4]['1%'])
            st.warning(warn_message)

        progress_bar.progress(100)
    
    else:
        # Iterating over different stationarity transformations
        absolute_test = transformer.test_absolute_data()
        progress_bar.progress(20)
        first_difference_test = transformer.test_first_difference()
        progress_bar.progress(40)
        log_difference_test = transformer.test_log_difference()
        progress_bar.progress(60)
        log_transformation_test = transformer.test_log_transformation()
        progress_bar.progress(80)
        seasonal_difference_test = transformer.test_seasonal_difference()
        progress_bar.progress(100)
        seasonal_log_difference_test = transformer.test_seasonal_log_difference()

        # Generating a list with all transformations
        transformations = [absolute_test, first_difference_test, log_difference_test, 
                        log_transformation_test, seasonal_difference_test, seasonal_log_difference_test]

        # Best transformation so far. We start with the absolute and non-transformed data
        best_transformation = absolute_test

        # Iteranting over each transformation
        for transformation in transformations:
            if transformation[0] < best_transformation[0] and transformation[2] != None:
                best_transformation = transformation

    # Checking rolling statistics
    mean = best_transformation[1].rolling(window=best_transformation[7]).mean()
    std = best_transformation[1].rolling(window=best_transformation[7]).std()
    
    if plot_results:
        # Plotting rolling statistics
        fig = plt.figure(figsize=(10, 5))
        orig = plt.plot(best_transformation[1], color='green', label='Original')
        mean = plt.plot(mean, color='red', label='Mean')
        std = plt.plot(std, color='black', label='Std')
        plt.legend(loc='best')
        plt.title(f'Moving average and Standard Deviation ({best_transformation[2]})')
        st.pyplot()

    # Performing Dickey-Fuller test
    st.write(f'Best ADF Test Results ({best_transformation[2]})')
    stat_test_value = best_transformation[0][0]
    critical_value_1_perc = best_transformation[0][4]['1%']

    dfoutput = pd.Series(best_transformation[0][0:4], index=['Statistical Test', 'p-value', '#Lags used', 'Number of observations'])
    for key, value in best_transformation[0][4].items():
        dfoutput['Critical value {}'.format(key)] = value
    st.write(dfoutput)

    return timeseries, best_transformation[3], best_transformation[4], best_transformation[7], best_transformation[1], best_transformation[5], best_transformation[6]