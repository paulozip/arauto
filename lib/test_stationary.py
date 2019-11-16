import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st

from statsmodels.tsa.stattools import adfuller

def test_stationary(timeseries, plot_results=False, data_frequency=None):
    '''
    Augmented Dickey-Fuller Test in order to check if we have a stationary series

    This function will perform different transformations (log transformation, difference, seasonal difference, etc.),
    and then will apply the ADF Test. At the end of this process, this function will return (along with other things)
    the best transformed data based on the lowest significant statistical test.

    Args:
        timeseries (Pandas Series): a timeseries to be used for the statistical tests and transformations
        plot_results (bool): Wether or not to plot the best time series transformation
        data_frequency (str, optional): the frequency that the data was collected (daily, monthly, yearly, etc.)
    
    Return:
        original_timeseries (Pandas Series): the original time series passed to the function 
        d (int): suggested value to be used for d (i) terms 
        D (int): suggested value to be used for D (seasonal difference) terms 
        seasonality (int): the seasonal frequency that occurs in the time series. It's based on the data_frequency parameter
        timeseries (Pandas Series): a transformed time series based on the best stationarity transformation (differencing, log, etc.)
        transformation_function (function): the function that was used to transform the time series to be stationary. 
        It can be a lambda function or a Numpy Log function (np.log)
    '''
    seasonality_dict = {'Hourly': 24, 
                        'Daily': 30, 
                        'Monthly': 12, 
                        'Quarterly': 4, 
                        'Yearly': 10}

    original_timeseries = timeseries
    progress_bar = st.progress(0)
    transformation_function = lambda x: x
    label = None
    d = 0
    D = 0
    seasonality = seasonality_dict[data_frequency]
    
    # Testing non-transformed data first
    dftest = adfuller(original_timeseries, autolag='AIC')
    best_transformation = dftest

    test_stationarity_code = '''
            # Applying Augmented Dickey-Fuller test
            dftest = adfuller(df, autolag='AIC')
                '''

    ## Checking if the statistical test is lower than 99% critical value
    if dftest[0] < dftest[4]['1%']:
        label = 'Absolute'

    # Else, try with DIFFERENCE
    progress_bar.progress(20)
    dftest = adfuller(original_timeseries.diff().dropna(), autolag='AIC')

    if dftest[0] < dftest[4]['1%'] and dftest[0] < best_transformation[0]:
        timeseries = original_timeseries.diff().dropna()
        best_transformation = dftest
        label = 'Difference'
        d = 1
        D = 0

        test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                dftest = adfuller(df.diff().dropna(), autolag='AIC')
                    '''
    
    # LOG TRANSFORMATION
    progress_bar.progress(40)
    dftest = adfuller(np.log(original_timeseries), autolag='AIC')
    if dftest[0] < dftest[4]['1%'] and dftest[0] < best_transformation[0]:
        timeseries = np.log(original_timeseries)
        transformation_function = np.log
        best_transformation = dftest
        label = 'Log transformation'
        d = 0
        D = 0

        test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                df = np.log(df) 
                dftest = adfuller(np.log(df), autolag='AIC')
                    '''

    # SEASONAL DIFFERENCE
    progress_bar.progress(60)
    dftest = adfuller(original_timeseries.diff(seasonality).dropna(), autolag='AIC')
    if dftest[0] < dftest[4]['1%'] and dftest[0] < best_transformation[0]:
        timeseries = original_timeseries.diff(seasonality).dropna()
        transformation_function = lambda x: x
        best_transformation = dftest
        label = 'Seasonality Difference'
        d = 0
        D = 1

        test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                dftest = adfuller(df.diff({}).dropna(), autolag='AIC')
                    '''.format(seasonality)
    
    # LOG DIFFERENCE
    progress_bar.progress(80)
    dftest = adfuller(np.log(original_timeseries).diff().dropna(), autolag='AIC')
    if dftest[0] < dftest[4]['1%'] and dftest[0] < best_transformation[0]:
        timeseries = np.log(original_timeseries).diff().dropna()
        transformation_function = np.log
        best_transformation = dftest
        label = 'Log Difference'
        d = 1
        D = 0
    
        test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                df = np.log(df)
                dftest = adfuller(df.diff().dropna(), autolag='AIC')
                    '''
        
    # SEASONAL LOG DIFFERENCE
    progress_bar.progress(100)
    dftest = adfuller(np.log(original_timeseries).diff().diff(seasonality).dropna(), autolag='AIC')
    if dftest[0] < dftest[4]['1%'] and dftest[0] < best_transformation[0]:
        timeseries = np.log(original_timeseries).diff().diff(seasonality).dropna()
        transformation_function = np.log
        best_transformation = dftest
        label = 'Seasonal Log Difference'
        d = 1
        D = 1

        test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                df = np.log(df)
                dftest = adfuller(df.diff().diff({}).dropna(), autolag='AIC')
                '''.format(seasonality)

    # Checking rolling statistics
    mean = timeseries.rolling(window=seasonality).mean()
    std = timeseries.rolling(window=seasonality).std()
    
    if plot_results:
        # Plotting rolling statistics
        fig = plt.figure(figsize=(10, 5))
        orig = plt.plot(timeseries, color='green', label='Original')
        mean = plt.plot(mean, color='red', label='Mean')
        std = plt.plot(std, color='black', label='Std')
        plt.legend(loc='best')
        plt.title(f'Moving average and Standard Deviation ({label})')
        st.pyplot()

    # Performing Dickey-Fuller test
    st.write(f'Best ADF Test Results ({label})')
    stat_test_value = best_transformation[0]
    critical_value_1_perc = best_transformation[4]['1%']

    dfoutput = pd.Series(best_transformation[0:4], index=['Statistical Test', 'p-value', '#Lags used', 'Number of observations'])
    for key, value in best_transformation[4].items():
        dfoutput['Critical value {}'.format(key)] = value
    st.write(dfoutput)

    return original_timeseries, d, D, seasonality, timeseries, transformation_function, test_stationarity_code