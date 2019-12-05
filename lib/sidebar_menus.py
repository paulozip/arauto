import streamlit as st
import sys

def sidebar_menus(menu_name, test_set_size=None, seasonality=None, terms=(0, 0, 0, 0, 0, 0, 0), df=None):
    '''
    Generates the sidebar menus for Streamlit. Based on menu_name parameter, it returns different menus for each situation.

    Args.
        menu_name (str): a menu name that will be shown on the sidebar. It can be: absolute, seasonal, adfuller, train_predictions,
        test_predictions, feature_target, or terms
        seasonality (str, optional): a value to be replaced by a number. e.g.: if Hourly, this function will consider 24 for seasonality
        terms (7-value tuple): tuple with 7 integer values for p, d, q, P, D, Q, and s
        df (Pandas DataFrame, optional): a Pandas DataFrame containing some time series data to extract the columns
    '''
    seasonality_dict = {'Hourly': 24, 
                        'Daily': 7, 
                        'Monthly': 12, 
                        'Quarterly': 4, 
                        'Yearly': 5}

    if menu_name == 'absolute':
        show_absolute_plot = st.sidebar.checkbox('Historical data', value=True)
        return show_absolute_plot
    elif menu_name == 'seasonal':
        show_seasonal_decompose = st.sidebar.checkbox('Seasonal decompose', value=True)
        return show_seasonal_decompose
    elif menu_name == 'adfuller':
        show_adfuller = st.sidebar.checkbox('Dickey-Fuller statistical test', value=True)
        return show_adfuller
    elif menu_name == 'train_predictions':
        show_train_predict_plot = st.sidebar.checkbox('Train set predictions', value=True)
        return show_train_predict_plot
    elif menu_name == 'test_predictions':
        show_test_predict_plot = st.sidebar.checkbox('Test set forecast', value=True)
        return show_test_predict_plot
    elif menu_name == 'feature_target':
        data_frequency = st.sidebar.selectbox('What is the FREQUENCY of your data? ', ['Select a frequency', 'Hourly', 'Daily', 'Monthly', 'Quarterly', 'Yearly'], 0)
        
        # If the frequency do not select a frequency for the dataset, it will raise an error
        if data_frequency == 'Select a frequency':
            # Hiding traceback in order to only show the error message
            sys.tracebacklimit = 0
            raise ValueError('Please, select the FREQUENCY for your data')
        
        # Show traceback error
        sys.tracebacklimit = None

        st.sidebar.markdown('### Choosing columns')
        ds_column = st.sidebar.selectbox('Which one is your DATE column?', df.columns, 0)
        y = st.sidebar.selectbox('Which column you want to PREDICT?', df.columns, 1)
        exog_variables = st.sidebar.multiselect('Which are your exogenous variables?', df.drop([ds_column, y], axis=1).columns)
        test_set_size = st.sidebar.slider('Validation set size', 3, 30, seasonality_dict[data_frequency])
        return ds_column, y, data_frequency, test_set_size, exog_variables
    elif menu_name == 'force_transformations':
        st.sidebar.markdown('### Force data transformation (optional)')
        transformation_techniques_list = ['Choose the best one', 'No transformation', 'First Difference', 
                                          'Log transformation', 'Seasonal Difference', 'Log First Difference', 
                                          'Log Difference + Seasonal Difference', 'Custom Difference']
        transformation_techniques = st.sidebar.selectbox('Transformation technique', transformation_techniques_list, 0)
        return transformation_techniques
    elif menu_name == 'terms':
        st.sidebar.markdown('### Model parameters')
        st.sidebar.text('Terms for (p, d, q)x(P, D, Q)s')
        p = st.sidebar.slider('p (AR)', 0, 30, min([terms[0], 30]))
        d = st.sidebar.slider('d (I)', 0, 3, min([terms[1], 3]))
        q = st.sidebar.slider('q (MA)', 0, 30, min([terms[2], 30]))
        P = st.sidebar.slider('P (Seasonal AR)', 0, 30, min([terms[3], 30]))
        D = st.sidebar.slider('D (Amount of seasonal difference)', 0, 3, min([terms[4], 3]))
        Q = st.sidebar.slider('Q (Seasonal MA)', 0, 30, min([terms[5], 30]))
        s = st.sidebar.slider('s (Seasonal frequency)', 0, 30, min([terms[6], 30]))
        
        st.sidebar.markdown('# Forecast periods')
        periods_to_forecast = st.sidebar.slider('How many periods to forecast?', 1, int(len(df.iloc[:-test_set_size])/3), int(seasonality/2))
        
        grid_search = st.sidebar.checkbox('Find the best parameters for me')
        train_model = st.sidebar.button('Do your Magic!')

        return p, d, q, P, D, Q, s, train_model, periods_to_forecast, grid_search