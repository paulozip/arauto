import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import streamlit as st
import sys

sys.path.insert(0, 'lib/')
#sys.tracebacklimit = 0 # Hide traceback on errors

from decompose_series import decompose_series
from file_selector import file_selector
from find_acf_pacf import find_acf_pacf
from generate_code import generate_code
from grid_search_arima import grid_search_arima
from mean_abs_pct_error import mean_abs_pct_error
from plot_forecast import plot_forecasts
from predict_set import predict_set
from sidebar_menus import sidebar_menus
from test_stationary import test_stationary
from train_ts_model import train_ts_model
from transform_time_series import transform_time_series

pd.set_option('display.float_format', lambda x: '%.3f' % x) # Granting that pandas won't use scientific notation for floating fields

description =   '''
                **Arauto** is an open-source project that will help you to forecast the future from historical data. 
                It uses statiscal models to give you accurated predictions for time series data, which is helpful for 
                financial data, network traffic, sales, and much more.
                '''
# Description
st.image('img/banner.png')
st.write('*An equivalent exchange: you give me data, I give you answers*')
st.write(description)

### SIDEBAR
st.sidebar.title('Your data')

filename, df = file_selector()

st.markdown('## **First lines of your data**')
st.dataframe(df.head(10)) # First lines of DataFrame

ds_column, y, data_frequency, test_set_size, exog_variables = sidebar_menus('feature_target', df=df)

# Name of the exogenous variables
exog_variables_names = exog_variables

# If there's not exogenous variables, it returns None
exog_variables = df[exog_variables] if len(exog_variables) > 0 else None

# Show plots
plot_menu_title = st.sidebar.markdown('### Charts')
plot_menu_text = st.sidebar.text('Select which charts you want to see')
show_absolute_plot = sidebar_menus('absolute')
show_seasonal_decompose = sidebar_menus('seasonal')
show_adfuller_test = sidebar_menus('adfuller')
show_train_prediction = sidebar_menus('train_predictions')
show_test_prediction = sidebar_menus('test_predictions')
force_transformation = sidebar_menus('force_transformations') # You can force a transformation technique

difference_size = None
seasonal_difference_size = None

if ('Custom Difference') in force_transformation:
    # If the user selects a custom transformation, enable the difference options
    difference_size = st.sidebar.slider('Difference size: ', 0, 30, 1)
    seasonal_difference_size = st.sidebar.slider('Seasonal Difference size: ', 0, 30, 1)

plot_adfuller_result = False
if show_adfuller_test:
    plot_adfuller_result = True

# Transform DataFrame to a Series
df = transform_time_series(df, ds_column, data_frequency, y)

# Show the historical plot?
if show_absolute_plot:
    st.markdown('# Historical data ')
    df[y].plot(color='green')
    plt.title('Absolute historical data')
    st.pyplot()

# Show decomposition plot
if show_seasonal_decompose:
    st.markdown('# Seasonal decomposition')
    decompose_series(df)

# Checking for stationarity in the series
st.title('Checking stationarity')

# If a function is not forced by the user, use the default pipeline
if force_transformation == None:
    ts, d, D, seasonality, acf_pacf_data, transformation_function, test_stationarity_code = test_stationary(df[y], plot_adfuller_result, data_frequency)
else:
    ts, d, D, seasonality, acf_pacf_data, transformation_function, test_stationarity_code = test_stationary(df[y], plot_adfuller_result, data_frequency, 
                                                                                                            force_transformation_technique = force_transformation, 
                                                                                                            custom_transformation_size = (difference_size, seasonal_difference_size))

st.title('ACF and PACF estimation')
p, q, P, Q = find_acf_pacf(acf_pacf_data, seasonality)
st.markdown('**Suggested parameters for your model**: {}x{}{}'.format((p, d, q), (P, D, Q), (seasonality)))

st.title('Time to train!')
st.write('Select the terms on the side bar and click "Do your Magic!" button')

try:
    p, d, q, P, D, Q, s, train_model, periods_to_forecast, execute_grid_search = sidebar_menus('terms', test_set_size, seasonality, (p, d, q, P, D, Q, seasonality), df=ts)
except ValueError:
    error_message = '''
                    A problem has occurred while we tried to find the best initial parameters for p, d, and q.
                    Please, check if your FREQUENCY field is correct for your dataset. For example, if your dataset
                    was collected in a daily basis, check if you selected DAILY in the FREQUENCY field.
                    '''
    raise ValueError(error_message)

# Showing a warning when Grid Search operation is too expensive
if execute_grid_search:
    if data_frequency in ['Hourly', 'Daily'] or p >= 5 or q >= 5:
        warning_grid_search = '''
                            Apply Grid Search on this dataset with these settings might be computationally expensive. 
                            Be sure you have enough memory for this operation, otherwise, it will fail
                            '''
        st.sidebar.warning(warning_grid_search)

# If train button has be clicked 
if train_model:
    exog_train = None
    exog_test = None

    # Aligning endog and exog variables index, if exog_variables is not null
    if type(exog_variables) == type(pd.DataFrame()):
        exog_variables.index = ts.index
        exog_train = exog_variables.iloc[:-test_set_size]
        exog_test = exog_variables.iloc[-test_set_size:]

    train_set = transformation_function(ts.iloc[:-test_set_size])

    test_set = transformation_function(ts.iloc[-test_set_size:])
    
    try:
        model = train_ts_model(train_set, p, d, q, P, D, Q, s, exog_variables=exog_train, quiet=False)
    except ValueError as ve:
        if ve.args[0] == 'maxlag should be < nobs':
            raise ValueError('Seems that you don\'t have enough data. Try to use smaller terms for AR and MA (p, q, P, Q)')
        else:
            raise ve

    st.markdown('## **Train set prediction**')
    st.write('The model was trained with this data. It\'s trying to predict the same data')
    if transformation_function == np.log1p:
        predict_set(train_set.iloc[-24:], y, seasonality, np.expm1, model, show_train_prediction=show_train_prediction, show_test_prediction=show_test_prediction)
    else:
        predict_set(train_set.iloc[-24:], y, seasonality, transformation_function, model, show_train_prediction=show_train_prediction, show_test_prediction=show_test_prediction)
    
    st.markdown('## **Test set forecast**')
    st.write('Unseen data. The model was not trained with this data and it\'s trying to forecast')
    if transformation_function == np.log1p:
        predict_set(test_set, y, seasonality, np.expm1, model, exog_variables=exog_test,forecast=True, show_train_prediction=show_train_prediction, show_test_prediction=show_test_prediction)
    else:
        predict_set(test_set, y, seasonality, transformation_function, model, exog_variables=exog_test, forecast=True, show_train_prediction=show_train_prediction, show_test_prediction=show_test_prediction)

    # Executing Grid Search
    if execute_grid_search:
        st.markdown('# Executing Grid Search')
        st.markdown('''
                    We\'re going to find the best parameters for your model. This might take some minutes. 
                    Now it's a good time to grab some coffee.
                    ''')
        p, d, q, P, D, Q, s = grid_search_arima(train_set, exog_train,  range(p+2), range(q+2), range(P+2), range(Q+2), d=d, D=D, s=s)
        
    # Creating final model
    st.warning('Training model with entire dataset. Please wait.')
    final_model = train_ts_model(transformation_function(ts), p, d, q, P, D, Q, s, exog_variables=exog_variables, quiet=True)
    
    # Forecasting data
    st.markdown('# Out-of-sample Forecast')
    
    if type(exog_variables) == type(pd.DataFrame()):
        st.write('You are using exogenous variables. We can\'t forecast the future since we don\'t have the exogenous variables for future periods. Adapt the code below to use them.' )
    else:
        if transformation_function == np.log1p:
            forecasts = np.expm1(final_model.forecast(periods_to_forecast))
            confidence_interval = np.expm1(final_model.get_forecast(periods_to_forecast).conf_int())

        else:
            forecasts = final_model.forecast(periods_to_forecast)
            confidence_interval = final_model.get_forecast(periods_to_forecast).conf_int()

        confidence_interval.columns = ['ci_lower', 'ci_upper']
        plot_forecasts(forecasts, confidence_interval, data_frequency)

    st.write('# Here\'s your code')
    st.markdown(generate_code(filename, ds_column, y, test_stationarity_code, test_set_size, 
                              seasonality, p, d, q, P, D, Q, s, exog_variables_names, transformation_function, 
                              periods_to_forecast, data_frequency))