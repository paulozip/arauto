import numpy as np

def generate_code(filename, ds_column, y, test_stationarity_code, test_set_size, 
                  seasonality, p, d, q, P, D, Q, s, exog_variables_names, transformation_function, 
                  periods_to_forecast, data_frequency):
    code_base = '''
                ```python

                import matplotlib.pyplot as plt
                import numpy as np
                import os
                import pandas as pd
                import plotly.graph_objs as go
                import statsmodels.api as sm

                from math import sqrt
                from plotly.offline import iplot, init_notebook_mode
                from sklearn.metrics import mean_squared_error, mean_absolute_error
                from statsmodels.tsa.seasonal import seasonal_decompose
                from statsmodels.tsa.stattools import adfuller

                # Granting that pandas will not use scientific notation for floating fields
                pd.set_option('display.float_format', lambda x: \'%.3f\' % x) 

                # Using Matplotlib figures inline
                %matplotlib inline

                # Setting Plot.ly to work on notebooks
                init_notebook_mode(connected=True)

                # Defining some functions
                def mean_abs_pct_error(actual_values, forecast_values):
                    \'\'\'
                    MAPE function to understand the average error percentage of the model

                    Args.:
                        actual_values (Numpy 1D Array, List or Iterable): True values of the set
                        forecast_values (Numpy 1D Array, List or Iterable): Values predicted by the model
                    Return:
                        MAPE value (float)
                    \'\'\'
                    err=0
                    for i in range(len(forecast_values)):
                        err += np.abs(actual_values.values[i] - forecast_values.values[i]) / actual_values.values[i]
                    return err * 100/len(forecast_values)

                def decompose_series(ts):
                    \'\'\'
                    This function applies a seasonal decomposition to a time series. It will generate a season plot, a trending plot, and, finally, a resid plot

                    Args.
                        ts (Pandas Series): a time series to be decomposed
                    \'\'\'
                    fig = plt.Figure(figsize=(12,7))
                    ax1 = plt.subplot(311)
                    ax2 = plt.subplot(312)
                    ax3 = plt.subplot(313)

                    decomposition = seasonal_decompose(ts)

                    decomposition.seasonal.plot(ax=ax1, title='Seasonality')
                    plt.legend('')

                    decomposition.trend.plot(ax=ax2, title='Trending')
                    plt.legend('')
                    
                    decomposition.resid.plot(ax=ax3, title='Resid')
                    plt.legend('')

                    plt.subplots_adjust(hspace=1)
                    plt.show()

                def find_acf_pacf(timeseries, seasonality):
                    \'\'\'
                    Function to find the amount of terms for p and q
                    Args.
                        timeseries (Pandas Series): a time series to estimate the p and q terms
                        seasonality (int): the seasonality is used to estimate the amount of lags to consider. By default, this function will use seasonality * 2 lags
                            to compute ACF and PACF
                    \'\'\'
                    
                    fig = plt.Figure(figsize=(12,7))
                    ax1 = plt.subplot(211)
                    ax2 = plt.subplot(212)

                    # Ploting the ACF function
                    sm.graphics.tsa.plot_acf(timeseries.dropna(), lags = seasonality * 2, ax=ax1)
                    
                    # Ploting the PACF function
                    sm.graphics.tsa.plot_pacf(timeseries.dropna(), lags = seasonality * 2, ax=ax2)
                    
                    plt.subplots_adjust(hspace=.4)
                    plt.show()
                
                def predict_set(timeseries, y, seasonality, transformation_function, model, forecast=False):
                    \'\'\'
                    Predicts the in-sample train observations

                    Args.
                        timeseries (Pandas Series): a time series that was used to fit a model
                        y (str): the target column
                        seasonality (int): the seasonality frequency
                        transformation_function (func): a function used to transform the target values
                        model (Statsmodel object): a fitted model
                        forecast (bool): wether or not forecast the test set
                    \'\'\'
                    timeseries = timeseries.to_frame()
                    timeseries[y] = transformation_function(timeseries[y])

                    if forecast:
                        timeseries['ŷ'] = transformation_function(model.forecast(len(timeseries)))
                    else:
                        timeseries['ŷ'] = transformation_function(model.predict())
                    
                    timeseries[[y, 'ŷ']].iloc[-(seasonality*3):].plot()

                    plt.ylabel(y)
                    plt.xlabel('')
                    plt.title('Train set predictions')
                    plt.show()

                    rmse = sqrt(mean_squared_error(timeseries[y].iloc[-(seasonality*3):], 
                                                   timeseries['ŷ'].iloc[-(seasonality*3):]))
                    aic = model.aic
                    bic = model.bic
                    hqic = model.hqic
                    mape = np.round(mean_abs_pct_error(timeseries[y].iloc[-(seasonality*3):], 
                                    timeseries['ŷ'].iloc[-(seasonality*3):]), 2)
                    mae = np.round(mean_absolute_error(timeseries[y].iloc[-(seasonality*3):], 
                                   timeseries['ŷ'].iloc[-(seasonality*3):]), 2)
                    
                    metrics_df = pd.DataFrame(data=[rmse, aic, bic, hqic, mape, mae], 
                                              columns = ['DATASET METRICS'], 
                                              index = ['RMSE', 'AIC', 'BIC', 'HQIC', 'MAPE', 'MAE'])
                    print(metrics_df)

                def grid_search(train_data, exog,  p_range, q_range, P_range, Q_range, d=1, D=1, s=12):
                    \'\'\'
                    Grid search for SARIMAX models. This is a time consuming function that will iterate
                    over different terms for AR and MA.

                    Args:
                        train_data (Pandas Series, Numpy Array, iterable): the training data containing endog variables
                        exog (Pandas Series, Numpy Array, iterable): exogenous variables
                        p_range (iterable): range of terms for p
                        d_range (int): differencing terms
                        q_range (iterable): range of terms for q
                        P_range (iterable): range of terms for Q
                        D_range (int): seasonal differencing terms
                        Q_range (iterable): range of terms for Q
                        s (int): seasonal frequency
                    Return:
                        current_best_model (Statsmodels SARIMAX results): a model with the best parameters, 
                            based on AIC, BIC, and HQIC metrics
                        models (list): all past models metrics for each iteractions
                    \'\'\'
                    best_model_aic = np.Inf 
                    best_model_bic = np.Inf 
                    best_model_hqic = np.Inf
                    best_model_order = (0, 0, 0)
                    models = []

                    for p_ in p_range:
                        for q_ in q_range:
                            for P_ in P_range:
                                for Q_ in Q_range:
                                    try:
                                        no_of_lower_metrics = 0
                                        model = sm.tsa.statespace.SARIMAX(endog = train_data,
                                                                        order = (p_, d, q_),
                                                                        exog = exog,
                                                                        seasonal_order = (P_, D, Q_, s),
                                                                        enforce_invertibility=False).fit()
                                        models.append(model)
                                        if model.aic <= best_model_aic: no_of_lower_metrics += 1
                                        if model.bic <= best_model_bic: no_of_lower_metrics += 1
                                        if model.hqic <= best_model_hqic:no_of_lower_metrics += 1
                                        if no_of_lower_metrics >= 2:
                                            best_model_aic = np.round(model.aic,0)
                                            best_model_bic = np.round(model.bic,0)
                                            best_model_hqic = np.round(model.hqic,0)
                                            best_model_order = (p_,d,q_,P_,D,Q_,s)
                                            current_best_model = model
                                            models.append(model)
                                            print("Best model so far: SARIMA" + str(best_model_order) + 
                                                "AIC: {{}} BIC: {{}} HQIC: {{}}".format(best_model_aic,best_model_bic,best_model_hqic)+
                                                "Resid: {{}}".format(np.round(np.expm1(current_best_model.resid).mean(), 3)))
                                    except:
                                        pass

                    print('\\n')
                    print(current_best_model.summary())                
                    return current_best_model, models

                def plot_forecasts(forecasts, confidence_interval, periods):
                    \'\'\'
                    Generate a plot with the forecasted observations

                    Args.
                        forecasts (Pandas Series): out-of-sample observations
                        confidence_interval (Pandas DataFrame): DataFrame containing a column for the lower boundary and another for the upper boundary 
                        periods (int): how much periods to forecast?
                    \'\'\'
                    lower_ci = dict(x = confidence_interval.index, 
                                    y = confidence_interval['ci_lower'], 
                                    line = dict(
                                            color = '#1EBC61', 
                                            shape = 'linear',
                                            width = 0.1
                                                ), 
                                    mode = 'lines',
                                    name = 'Lower 95% CI', 
                                    showlegend = False, 
                                    type = "scatter", 
                                    xaxis = 'x', 
                                    yaxis = 'y')
                    upper_ci = dict(x = confidence_interval.index, 
                                    y = confidence_interval['ci_upper'], 
                                    fill = 'tonexty', 
                                    line = dict(
                                            color = '#1EBC61', 
                                            shape = 'linear',
                                            width = 0.1
                                                ), 
                                    mode = 'lines', 
                                    name = 'Upper 95% CI', 
                                    type = 'scatter', 
                                    xaxis = 'x', 
                                    yaxis = 'y')
                    forecasting =  dict(x = forecasts.index, 
                                        y = forecasts.values,
                                        line = dict(
                                                color = '#005C01', 
                                                shape = 'linear',
                                                width = 3
                                                ), 
                                    mode = 'lines', 
                                    name = 'Forecasting', 
                                    type = 'scatter', 
                                    xaxis = 'x', 
                                    yaxis = 'y')

                    plot_data = ([lower_ci, upper_ci, forecasting])
                    layout = go.Layout(title = str(periods) + ' Forecasts')
                    fig = go.Figure(data = plot_data, layout=layout)
                    iplot(fig)
                
                # Reading dataset
                df = pd.read_csv('{0}')
                '''.format(filename)

    transform_time_series = '''
                # Reading dataset
                df.set_index('{}', inplace = True)
                df.index = df.index.astype('datetime64[ns]')
                print(df.head())

                # Plotting your historical data
                df.plot(color='green')
                plt.title('Absolute historical data')
                plt.show()

                # Creating exogenous variables
                exogenous_variables = {}

                # Transforming data to a series
                df = df['{}']            
                            '''.format(ds_column, 
                                       'df[{}]'.format(exog_variables_names) if len(exog_variables_names) > 0 else None, 
                                       y)

    test_stationarity = test_stationarity_code

    rolling_statistics =   '''
                # Checking rolling statistics
                mean = df.rolling(window={0}).mean()
                std = df.rolling(window={0}).std()

                # Plotting rolling statistics
                fig = plt.figure(figsize=(10, 5))
                orig = plt.plot(df, color='green', label='Original')
                mean = plt.plot(mean, color='red', label='Mean')
                std = plt.plot(std, color='black', label='Std')

                plt.legend(loc='best')
                plt.title(f'Moving average and Standard Deviation')
                plt.show()
                            '''.format(seasonality)

    dickey_fuller_test = '''
                # Performing Dickey-Fuller test
                print('Best ADF Test Results')
                critical_value_1_perc = dftest[4]['1%']

                dfoutput = pd.Series(dftest[0:4], index=['Statistical Test', 'p-value', '#Lags used', 'Number of observations'])
                for key, value in dftest[4].items():
                    dfoutput['Critical value ' + key] = value
                print(dfoutput)
                         '''
    
    preprocessing_code = '''
                train_transformation_func = {0}
                train_set = train_transformation_func(df.iloc[:-{1}])
                test_set = train_transformation_func(df.iloc[-{1}:])
                         '''.format('np.log1p' if transformation_function == np.log1p else 'lambda x: x', test_set_size)

    train_model = f'''
                # Training model
                mod = sm.tsa.statespace.SARIMAX(df,
                                                order = ({p}, {d}, {q}),
                                                exog = exogenous_variables,
                                                seasonal_order = ({P}, {D}, {Q}, {s}),
                                                enforce_invertibility=False)
                # Fitting model
                try:
                    mod = mod.fit()
                except np.linalg.LinAlgError:
                    mod = sm.tsa.statespace.SARIMAX(df,
                                                order = ({p}, {d}, {q}),
                                                exog = exogenous_variables,
                                                seasonal_order = ({P}, {D}, {Q}, {s}),
                                                enforce_invertibility=False,
                                                initialization='approximate_diffuse')
                    mod = mod.fit()
                print(mod.summary())

                ## Uncomment this part to use Grid Search (computational expensive)
                #grid_search(df, exogenous_variables, range({p+3}), {d}, range({q+3}), range({P+3}), {D}, range({Q+3}), {s})
                  '''.format(p, d, q, P, D, Q, s)
    
    predict_set = '''
                predict_set(df, '{}', {}, {}, mod)
                  '''.format(y, seasonality, 'np.log1p' if transformation_function == np.log1p else 'lambda x: x')

    forecasting_code =  '''
                # Forecasting out-of-sample periods
                forecasts = np.expm1(mod.forecast({0}))
                confidence_interval = np.expm1(mod.get_forecast({0}).conf_int())
                
                # Generating confidence interval and plotting forecasting
                confidence_interval.columns = ['ci_lower', 'ci_upper']
                plot_forecasts(forecasts, confidence_interval, '{1}')
                        '''.format(periods_to_forecast, data_frequency)

    final_code = code_base + transform_time_series + test_stationarity + rolling_statistics + dickey_fuller_test + preprocessing_code + train_model + predict_set + forecasting_code
    return final_code
