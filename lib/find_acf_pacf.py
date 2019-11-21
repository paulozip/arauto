import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import streamlit as st

def find_acf_pacf(timeseries, seasonality):
    '''
    Function to find the amount of terms for p and q
    Args.
        timeseries (Pandas Series): a time series to estimate the p and q terms
        seasonality (int): the seasonality is used to estimate the amount of lags to consider. By default, this function will use seasonality * 2 lags
            to compute ACF and PACF
    '''
    
    fig = plt.figure(figsize=(10,5))
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)
    
    p_terms = 0
    q_terms = 0
    P_terms = 0
    Q_terms = 0

    lower_conf_int = -1.96/np.sqrt(len(timeseries.dropna()))
    upper_conf_int = 1.96/np.sqrt(len(timeseries.dropna()))

    pacf_values = sm.tsa.stattools.pacf(timeseries.dropna(), nlags = seasonality * 2, method='ywunbiased')

    acf_values = sm.tsa.stattools.acf(timeseries.dropna(), nlags = seasonality * 2, fft=False, unbiased=False)

    #st.write(pacf_values, lower_conf_int)

    # Checking for p terms
    for value in pacf_values[1:]:
        if value >= upper_conf_int or value <= lower_conf_int:
            p_terms += 1
        else:
            break
    
    # Checking for q terms
    for value in acf_values[1:]:
        if value >= upper_conf_int or value <= lower_conf_int:
            q_terms += 1
        else:
            break

    # Checking for P terms
    if pacf_values[seasonality] >= upper_conf_int or pacf_values[seasonality] <= lower_conf_int:
        P_terms += 1
        if pacf_values[seasonality*2] >= upper_conf_int or pacf_values[seasonality*2] <= lower_conf_int:
            P_terms += 1

    # Checking for Q terms
    if acf_values[seasonality] >= upper_conf_int or acf_values[seasonality] <= lower_conf_int:
        Q_terms += 1
        if acf_values[seasonality*2] >= upper_conf_int or acf_values[seasonality*2] <= lower_conf_int:
            Q_terms += 1

    # Ploting the ACF function
    sm.graphics.tsa.plot_acf(timeseries.dropna(), lags = seasonality * 2, ax=ax1, color='green')
    
    # Ploting the PACF function
    sm.graphics.tsa.plot_pacf(timeseries.dropna(), lags = seasonality * 2, ax=ax2, color='green')
    
    plt.subplots_adjust(hspace=.4)
    st.pyplot()

    return p_terms, q_terms, P_terms, Q_terms