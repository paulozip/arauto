import numpy as np

from statsmodels.tsa.stattools import adfuller

class timeSeriesTransformer:
    def __init__(self, original_timeseries, data_frequency):
        self.seasonality_dict = {'Hourly': 24, 
                                 'Daily': 30, 
                                 'Monthly': 12, 
                                 'Quarterly': 4, 
                                 'Yearly': 10}
        self.seasonality = self.seasonality_dict[data_frequency]
        self.original_timeseries = original_timeseries
        self.transformed_time_series = original_timeseries
        self.test_stationarity_code = None
        self.transformation_function = lambda x: x
        self.label = None
        self.d = 0
        self.D = 0
    
    def test_absolute_data(self):
        '''
        Run the Adfuller test on the original data, without transformation
        '''
        self.dftest = adfuller(self.original_timeseries, autolag='AIC')
        #self.best_transformation = self.dftest
        
        self.test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                dftest = adfuller(df, autolag='AIC')
                    '''
        self.label = 'Absolute' if self.dftest[0] < self.dftest[4]['1%'] else None
        
        #return self.label, self.d, self.D, self.transformation_function

    def test_first_difference(self):
        self.dftest = adfuller(self.original_timeseries.diff().dropna(), autolag='AIC')
        #self.best_transformation = self.dftest
        self.transformed_time_series = self.original_timeseries.diff().dropna()

        self.test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                dftest = adfuller(df.diff().dropna(), autolag='AIC')
                    '''
        self.label = 'Difference' if self.dftest[0] < self.dftest[4]['1%'] else None
        self.d = 1
        self.D = 0
        
        #return self.label, self.d, self.D, self.transformation_function
        
    def test_log_transformation(self):
        self.dftest = adfuller(np.log(self.original_timeseries), autolag='AIC')
        self.transformed_time_series = np.log(self.original_timeseries)
        self.transformation_function = np.log

        self.test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                df = np.log(df) 
                dftest = adfuller(np.log(df), autolag='AIC')
                    '''
        self.label = 'Log transformation' if self.dftest[0] < self.dftest[4]['1%'] else None
        self.d = 0
        self.D = 0

    def test_seasonal_difference(self):
        self.dftest = adfuller(self.original_timeseries.diff(self.seasonality).dropna(), autolag='AIC')
        self.transformed_time_series = self.original_timeseries.diff(self.seasonality).dropna()
        self.transformation_function = lambda x: x

        self.test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                dftest = adfuller(df.diff({}).dropna(), autolag='AIC')
                    '''.format(self.seasonality)
        self.label = 'Seasonality Difference' if self.dftest[0] < self.dftest[4]['1%'] else None
        self.d = 0
        self.D = 1
    
    def test_log_difference(self):
        self.dftest = adfuller(np.log(self.original_timeseries).diff().dropna(), autolag='AIC')
        self.transformed_time_series = np.log(self.original_timeseries).diff().dropna()
        self.transformation_function = np.log

        self.test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                df = np.log(df)
                dftest = adfuller(df.diff().dropna(), autolag='AIC')
                    '''
        self.label = 'Log Difference' if self.dftest[0] < self.dftest[4]['1%'] else None
        self.d = 1
        self.D = 0
    
    def test_seasonal_log_difference(self):
        self.dftest = adfuller(np.log(self.original_timeseries).diff().diff(self.seasonality).dropna(), autolag='AIC')
        self.transformed_time_series = np.log(self.original_timeseries).diff().diff(self.seasonality).dropna()
        self.transformation_function = np.log

        self.test_stationarity_code = '''
                # Applying Augmented Dickey-Fuller test
                df = np.log(df)
                dftest = adfuller(df.diff().diff({}).dropna(), autolag='AIC')
                '''.format(self.seasonality)

        self.label = 'Seasonal Log Difference' if self.dftest[0] < self.dftest[4]['1%'] else None
        self.d = 1
        self.D = 1