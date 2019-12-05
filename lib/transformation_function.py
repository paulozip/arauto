import numpy as np

from statsmodels.tsa.stattools import adfuller

class timeSeriesTransformer:
    def __init__(self, original_timeseries, data_frequency):
        self.seasonality_dict = {'Hourly': 24, 
                                 'Daily': 7, 
                                 'Monthly': 12, 
                                 'Quarterly': 4, 
                                 'Yearly': 5}
        self.seasonality = self.seasonality_dict[data_frequency]
        self.original_timeseries = original_timeseries
        self.transformed_time_series = original_timeseries
        self.test_stationarity_code = None
        self.transformation_function = lambda x: x
        self.label = None
        self.d = 0
        self.D = 0

    def test_custom_difference(self, custom_transformation_size):
        self.d = custom_transformation_size[0]
        self.D = custom_transformation_size[1]

        self.transformed_time_series = self.original_timeseries.diff(self.d).diff(self.seasonality * self.D).dropna()
        self.dftest = adfuller(self.transformed_time_series, autolag='AIC')
        self.transformation_function = lambda x: x

        self.test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                dftest = adfuller(df.diff({}).diff({}).dropna(), autolag='AIC')
                '''.format(self.d, self.D)

        self.label = 'Custom Difference' if self.dftest[0] < self.dftest[4]['1%'] else None

        return self.dftest, self.transformed_time_series, self.label, self.d, self.D, self.transformation_function, self.test_stationarity_code, self.seasonality
    
    def test_absolute_data(self):
        '''
        Run the Adfuller test on the original data, without transformation

        Returns:
            dftest (tuple): a tuple containing the Augmented Dickey-Fuller test. Among other things, 
                it contains the test statistics, the critical values, and p-values. Please refer to 
                (https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.adfuller.html) for
                further information
            transformed_time_series (pandas Series): the transformed time series if applied. For this function,
                it returns the original time series, since no transformations are applied. 
            label (str): if the adfuller result is statistical significant, a string is returned informing the
                transformation that was applied to the time series. This informations is only needed to inform on
                Matplotlib plots in test_stationarity function 
            d (int): the amount of integrated terms used in this function/transformation. For this function, no differencing is
                applied, since it returns the original time series 
            D (int): the amount of seasonal integrated terms used in this function/transformation. For this function, no differencing is
                applied, since it returns the original time series
            transformation_function (func): this module contains two distinct transformation functions: numpy.log and lambda x: x.
                This value informs what transformation function was used on the time series. If Logarithm was used, returns numpy.log,
                otherwise, returns a lambda function 
            test_stationarity_code (str): the code that was used on this transformation. This is used in future to generate the code
                for the user on Arauto .
            seasonality (int): the amount of seasonality terms
        '''

        self.dftest = adfuller(self.original_timeseries, autolag='AIC')
        
        self.test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                dftest = adfuller(df, autolag='AIC')
                    '''
        self.label = 'Absolute' if self.dftest[0] < self.dftest[4]['1%'] else None
        
        return self.dftest, self.transformed_time_series, self.label, self.d, self.D, self.transformation_function, self.test_stationarity_code, self.seasonality

    def test_first_difference(self):
        '''
        Run the Adfuller test on the original data with first difference

        Returns:
            dftest (tuple): a tuple containing the Augmented Dickey-Fuller test. Among other things, 
                it contains the test statistics, the critical values, and p-values. Please refer to 
                (https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.adfuller.html) for
                further information
            transformed_time_series (pandas Series): the transformed time series if applied.
            label (str): if the adfuller result is statistical significant, a string is returned informing the
                transformation that was applied to the time series. This informations is only needed to inform on
                Matplotlib plots in test_stationarity function 
            d (int): the amount of integrated terms used in this function/transformation.
            D (int): the amount of seasonal integrated terms used in this function/transformation.
            transformation_function (func): this module contains two distinct transformation functions: numpy.log and lambda x: x.
                This value informs what transformation function was used on the time series. If Logarithm was used, returns numpy.log,
                otherwise, returns a lambda function 
            test_stationarity_code (str): the code that was used on this transformation. This is used in future to generate the code
                for the user on Arauto .
            seasonality (int): the amount of seasonality terms
        '''

        self.transformed_time_series = self.original_timeseries.diff().dropna()
        self.dftest = adfuller(self.transformed_time_series, autolag='AIC')

        self.test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                dftest = adfuller(df.diff().dropna(), autolag='AIC')
                    '''
        self.label = 'Difference' if self.dftest[0] < self.dftest[4]['1%'] else None
        self.d = 1
        self.D = 0
        
        return self.dftest, self.transformed_time_series, self.label, self.d, self.D, self.transformation_function, self.test_stationarity_code, self.seasonality
        
    def test_log_transformation(self):
        '''
        Run the Adfuller test on the original data with log transformation

        Returns:
            dftest (tuple): a tuple containing the Augmented Dickey-Fuller test. Among other things, 
                it contains the test statistics, the critical values, and p-values. Please refer to 
                (https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.adfuller.html) for
                further information
            transformed_time_series (pandas Series): the transformed time series if applied.
            label (str): if the adfuller result is statistical significant, a string is returned informing the
                transformation that was applied to the time series. This informations is only needed to inform on
                Matplotlib plots in test_stationarity function 
            d (int): the amount of integrated terms used in this function/transformation.
            D (int): the amount of seasonal integrated terms used in this function/transformation.
            transformation_function (func): this module contains two distinct transformation functions: numpy.log and lambda x: x.
                This value informs what transformation function was used on the time series. If Logarithm was used, returns numpy.log,
                otherwise, returns a lambda function 
            test_stationarity_code (str): the code that was used on this transformation. This is used in future to generate the code
                for the user on Arauto .
            seasonality (int): the amount of seasonality terms
        '''

        self.transformed_time_series = np.log1p(self.original_timeseries)
        self.dftest = adfuller(self.transformed_time_series, autolag='AIC')
        self.transformation_function = np.log1p

        self.test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                df = np.log1p(df) 
                dftest = adfuller(np.log1p(df), autolag='AIC')
                    '''
        self.label = 'Log transformation' if self.dftest[0] < self.dftest[4]['1%'] else None
        self.d = 0
        self.D = 0

        return self.dftest, self.transformed_time_series, self.label, self.d, self.D, self.transformation_function, self.test_stationarity_code, self.seasonality

    def test_seasonal_difference(self):
        '''
        Run the Adfuller test on the original data with seasonal difference

        Returns:
            dftest (tuple): a tuple containing the Augmented Dickey-Fuller test. Among other things, 
                it contains the test statistics, the critical values, and p-values. Please refer to 
                (https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.adfuller.html) for
                further information
            transformed_time_series (pandas Series): the transformed time series if applied.
            label (str): if the adfuller result is statistical significant, a string is returned informing the
                transformation that was applied to the time series. This informations is only needed to inform on
                Matplotlib plots in test_stationarity function 
            d (int): the amount of integrated terms used in this function/transformation.
            D (int): the amount of seasonal integrated terms used in this function/transformation.
            transformation_function (func): this module contains two distinct transformation functions: numpy.log and lambda x: x.
                This value informs what transformation function was used on the time series. If Logarithm was used, returns numpy.log,
                otherwise, returns a lambda function 
            test_stationarity_code (str): the code that was used on this transformation. This is used in future to generate the code
                for the user on Arauto .
            seasonality (int): the amount of seasonality terms
        '''

        self.transformed_time_series = self.original_timeseries.diff(self.seasonality).dropna()
        self.dftest = adfuller(self.transformed_time_series, autolag='AIC')
        self.transformation_function = lambda x: x

        self.test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                dftest = adfuller(df.diff({}).dropna(), autolag='AIC')
                    '''.format(self.seasonality)
        self.label = 'Seasonality Difference' if self.dftest[0] < self.dftest[4]['1%'] else None
        self.d = 0
        self.D = 1

        return self.dftest, self.transformed_time_series, self.label, self.d, self.D, self.transformation_function, self.test_stationarity_code, self.seasonality
    
    def test_log_difference(self):
        '''
        Run the Adfuller test on the original data with log first difference transformation

        Returns:
            dftest (tuple): a tuple containing the Augmented Dickey-Fuller test. Among other things, 
                it contains the test statistics, the critical values, and p-values. Please refer to 
                (https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.adfuller.html) for
                further information
            transformed_time_series (pandas Series): the transformed time series if applied.
            label (str): if the adfuller result is statistical significant, a string is returned informing the
                transformation that was applied to the time series. This informations is only needed to inform on
                Matplotlib plots in test_stationarity function 
            d (int): the amount of integrated terms used in this function/transformation.
            D (int): the amount of seasonal integrated terms used in this function/transformation.
            transformation_function (func): this module contains two distinct transformation functions: numpy.log and lambda x: x.
                This value informs what transformation function was used on the time series. If Logarithm was used, returns numpy.log,
                otherwise, returns a lambda function 
            test_stationarity_code (str): the code that was used on this transformation. This is used in future to generate the code
                for the user on Arauto .
            seasonality (int): the amount of seasonality terms
        '''

        self.transformed_time_series = np.log1p(self.original_timeseries).diff().dropna()
        self.dftest = adfuller(self.transformed_time_series, autolag='AIC')
        self.transformation_function = np.log1p

        self.test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                df = np.log1p(df)
                dftest = adfuller(df.diff().dropna(), autolag='AIC')
                    '''
        self.label = 'Log Difference' if self.dftest[0] < self.dftest[4]['1%'] else None
        self.d = 1
        self.D = 0

        return self.dftest, self.transformed_time_series, self.label, self.d, self.D, self.transformation_function, self.test_stationarity_code, self.seasonality
    
    def test_seasonal_log_difference(self):
        '''
        Run the Adfuller test on the original data with seasonal difference and log first difference

        Returns:
            dftest (tuple): a tuple containing the Augmented Dickey-Fuller test. Among other things, 
                it contains the test statistics, the critical values, and p-values. Please refer to 
                (https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.adfuller.html) for
                further information
            transformed_time_series (pandas Series): the transformed time series if applied.
            label (str): if the adfuller result is statistical significant, a string is returned informing the
                transformation that was applied to the time series. This informations is only needed to inform on
                Matplotlib plots in test_stationarity function 
            d (int): the amount of integrated terms used in this function/transformation.
            D (int): the amount of seasonal integrated terms used in this function/transformation.
            transformation_function (func): this module contains two distinct transformation functions: numpy.log and lambda x: x.
                This value informs what transformation function was used on the time series. If Logarithm was used, returns numpy.log,
                otherwise, returns a lambda function 
            test_stationarity_code (str): the code that was used on this transformation. This is used in future to generate the code
                for the user on Arauto .
            seasonality (int): the amount of seasonality terms
        '''

        self.transformed_time_series = np.log1p(self.original_timeseries).diff().diff(self.seasonality).dropna()
        self.dftest = adfuller(self.transformed_time_series, autolag='AIC')
        self.transformation_function = np.log1p

        self.test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                df = np.log1p(df)
                dftest = adfuller(df.diff().diff({}).dropna(), autolag='AIC')
                '''.format(self.seasonality)

        self.label = 'Log Difference + Seasonal Difference' if self.dftest[0] < self.dftest[4]['1%'] else None
        self.d = 1
        self.D = 1

        return self.dftest, self.transformed_time_series, self.label, self.d, self.D, self.transformation_function, self.test_stationarity_code, self.seasonality