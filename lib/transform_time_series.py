from numpy import isscalar
from pandas import DatetimeIndex, date_range, merge
from streamlit import warning
from statsmodels.tsa.seasonal import seasonal_decompose

import statsmodels.api as sm

def test_time_series(ts):
    '''
    This function will test the transformed time series with a decomposition and a model training. 
    This will ensure that the data a proper format to be used in the rest of the project. This is a crucial
    step to understand if the time series has a valid datetime index (used by decomposition function and ARIMA)
    '''
    
    # Decomposing series. A datetime index is required for this function. 
    # If it raise an error, the time series doesn't have a datetime index
    seasonal_decompose(ts)

    # Training a simple model
    mod = sm.tsa.statespace.SARIMAX(ts, order = (0, 0, 1))
    results = mod.fit()

    # Returns an error if the forecasts index is a scalar
    assert not isscalar(results.forecast(10).index[0]), 'The forecasts index is not a datetime type'

def transform_time_series(df, ds_column, date_frequency, y):
    '''
    Transforms a Pandas DataFrame into a Pandas Series, using a column as the index

    Args:
        df (Pandas DataFrame): a DataFrame to be transformed
        ds_column (str): column name that will be used as an index
        date_frequency (str): the frequency of the dataset. It could be daily, monthly, etc.

    Return:
        df (Pandas Series): transformed DataFrame
    '''

    date_frequency_dict = {'Hourly': 'H', 
                           'Daily': 'D',
                           'Monthly': 'MS', 
                           'Quarterly': 'Q', 
                           'Yearly': 'Y'}
    
    df.set_index(ds_column, inplace = True)
    df = df.dropna()
    try:
        # Try to make a simple convertion
        df.index = df.index.astype('datetime64[ns]')
        test_time_series(df[y])
    except:
        # If not pass, get the index frequency
        try:
            date_format = DatetimeIndex(df.index[-10:], freq='infer')

            # Try to apply the date frequency to data
            df.index = df.asfreq(date_format.freq, fill_value=0)
            test_time_series(df[y])
        # This errors occurs when it finds null values
        except ValueError:
            try:
                # Creating dataframe to fill the missing dates
                fill_date_range = date_range(df.index.min(), df.index.max(), freq=date_format.freq)
                df = merge(fill_date_range.to_frame().drop(0, axis=1), 
                           df, 
                           how = 'left', 
                           right_index = True, 
                           left_index = True)
                # Filling null values
                null_values = df[df.loc[:, y].isnull()].index.values
                if len(null_values) > 0:
                    warning('We found null values at {}. Filling it with zeros.'.format(null_values))
                    df = df.fillna(0)
                test_time_series(df[y])
            except:
                # If it doesn't work, try to infer the frequency based on the FREQUENCY field
                try:
                    warning_message = '''
                                We could not find the proper date frequency of this dataset. 
                                We will try to infer it based on the FREQUENCY field on the sidebar, but be sure that
                                this dataset is in one of the following formats (Hourly, Daily, Monthly, Quarterly, or Yearly)
                                '''
                    warning(warning_message)
                    df = df.asfreq(date_frequency_dict[date_frequency])
                    
                    # Filling null values
                    null_values = df[df.loc[:, y].isnull()].index.values
                    if len(null_values) > 0:
                        warning('We found null values at {}. Filling it with zeros.'.format(null_values))
                        df = df.fillna(0)
                    test_time_series(df[y])
                except:
                    error_message = '''
                                    There was a problem while we tried to convert the DATE column for a valid format.
                                    Be sure there is no null value in the DATE column and that it is in a valid format for Pandas to_datetime function. 
                                    Please, refer to (https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases) to know more abbout the
                                    date frequencies
                                    '''
                    raise TypeError(error_message)
    return df