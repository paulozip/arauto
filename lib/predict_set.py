import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from math import sqrt
from mean_abs_pct_error import mean_abs_pct_error
from sklearn.metrics import mean_squared_error, mean_absolute_error

def predict_set(timeseries, y, seasonality, transformation_function, model, exog_variables=None,forecast=False, show_train_prediction=None, show_test_prediction=None):
    '''
    Predicts the in-sample train observations

    Args.
        timeseries (Pandas Series): a time series that was used to fit a model
        y (str): the target column
        seasonality (int): the seasonality frequency
        transformation_function (func): a function used to transform the target values
        model (Statsmodel object): a fitted model
        exog_variables (Pandas DataFrame): exogenous (independent) variables of your model
        forecast (bool): wether or not forecast the test set
        show_train_prediction (bool): wether or not to plot the train set predictions
        show_test_prediction (bool): wether or not to plot the test set predictions
    '''
    timeseries = timeseries.to_frame()
    timeseries[y] = transformation_function(timeseries[y])

    if forecast:
        timeseries['ŷ'] = transformation_function(model.forecast(len(timeseries), exog=exog_variables))
    else:
        timeseries['ŷ'] = transformation_function(model.predict())
    
    if show_train_prediction and forecast == False:
        timeseries[[y, 'ŷ']].iloc[-(seasonality*3):].plot(color=['green', 'red'])

        plt.ylabel(y)
        plt.xlabel('')
        plt.title('Train set predictions')
        st.pyplot()
    elif show_test_prediction and forecast:
        timeseries[[y, 'ŷ']].iloc[-(seasonality*3):].plot(color=['green', 'red'])

        plt.ylabel(y)
        plt.xlabel('')
        plt.title('Test set predictions')
        st.pyplot()

    try:
        rmse = sqrt(mean_squared_error(timeseries[y].iloc[-(seasonality*3):], timeseries['ŷ'].iloc[-(seasonality*3):]))
        aic = model.aic
        bic = model.bic
        hqic = model.hqic
        mape = np.round(mean_abs_pct_error(timeseries[y].iloc[-(seasonality*3):], timeseries['ŷ'].iloc[-(seasonality*3):]), 2)
        mae = np.round(mean_absolute_error(timeseries[y].iloc[-(seasonality*3):], timeseries['ŷ'].iloc[-(seasonality*3):]), 2)
    except ValueError:
        error_message = '''
                        There was a problem while we calculated the model metrics. 
                        Usually this is due a problem with the format of the DATE column. 
                        Be sure it is in a valid format for Pandas to_datetime function
                        '''
        raise ValueError(error_message)
    
    metrics_df = pd.DataFrame(data=[rmse, aic, bic, hqic, mape, mae], columns = ['{} SET METRICS'.format('TEST' if forecast else 'TRAIN')], index = ['RMSE', 'AIC', 'BIC', 'HQIC', 'MAPE', 'MAE'])
    st.markdown('### **Metrics**')
    st.dataframe(metrics_df)