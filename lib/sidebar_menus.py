import streamlit as st

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
                        'Daily': 30, 
                        'Monthly': 12, 
                        'Quarterly': 4, 
                        'Yearly': 10}

    if menu_name == 'absolute':
        show_absolute_plot = st.sidebar.checkbox('Historical data')
        return show_absolute_plot
    elif menu_name == 'seasonal':
        show_seasonal_decompose = st.sidebar.checkbox('Seasonal decompose')
        return show_seasonal_decompose
    elif menu_name == 'adfuller':
        show_adfuller = st.sidebar.checkbox('Dickey-Fuller statistical test')
        return show_adfuller
    elif menu_name == 'train_predictions':
        show_train_predict_plot = st.sidebar.checkbox('Train set predictions')
        return show_train_predict_plot
    elif menu_name == 'test_predictions':
        show_test_predict_plot = st.sidebar.checkbox('Test set forecast')
        return show_test_predict_plot
    elif menu_name == 'feature_target':
        st.sidebar.markdown('### Choosing columns')
        ds_column = st.sidebar.selectbox('Which one is your DATE column?', df.columns, 0)
        y = st.sidebar.selectbox('Which column you want to PREDICT?', df.columns, 1)
        exog_variables = st.sidebar.multiselect('Which are your exogenous variables?', df.drop([ds_column, y], axis=1).columns)
        data_frequency = st.sidebar.selectbox('What frequency is your data? ', ['Hourly', 'Daily', 'Monthly', 'Quarterly', 'Yearly'], 1)
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
        p = st.sidebar.slider('p (AR)', 0, 10, terms[0])
        d = st.sidebar.slider('d (I)', 0, 3, terms[1])
        q = st.sidebar.slider('q (MA)', 0, 10, terms[2])
        P = st.sidebar.slider('P (Seasonal AR)', 0, 10, terms[3])
        D = st.sidebar.slider('D (Amount of seasonal difference)', 0, 3, terms[4])
        Q = st.sidebar.slider('Q (Seasonal MA)', 0, 10, terms[5])
        s = st.sidebar.slider('s (Seasonal frequency)', 0, 30, terms[6])
        
        st.sidebar.markdown('# Forecast periods')
        periods_to_forecast = st.sidebar.slider('How many periods to forecast?', 1, int(len(df.iloc[:-test_set_size])/3), int(seasonality/2))
        
        grid_search = st.sidebar.checkbox('Find the best parameters for me')
        train_model = st.sidebar.button('Do your Magic!')

        return p, d, q, P, D, Q, s, train_model, periods_to_forecast, grid_search