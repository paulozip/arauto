import numpy as np
import statsmodels.api as sm
import streamlit as st

def train_ts_model(Y, p, d, q, P, D, Q, s, exog_variables=None, quiet=False):
    '''
    A function to train a time series model using a SARIMAX estimator

    Args.
        Y (Pandas Series): a time series data to model. It must be a Pandas Series, where the index is the time series frequency and the values are
            the observations that will be model.
        p (int): amount of AR terms
        d (int): amount of differencing terms
        q (int): amount of MA terms
        P (int): amount of Autoregressive terms for seasonality
        D (int): amount of seasonal differencing terms
        Q (int): amount of Moving Average terms for seasonality
        s (int): seasonality frequency
        exog_variables (Pandas Series): exogenous variables to be used on the model
        quiet (bool), default False: if True, this function will just train the model, without showing the summary information
    Return:
        results (Statsmodel fitted model): a fitted model based on the parameters 
    '''
    waiting_messages = ['Training robots to conquer the world! Please, wait.',
                        'Training your model...',
                        'Training...Come with me if you wanna live.',
                        'Cooking the model. Please wait...',
                        'Zzzzzzzzz...',
                        'It takes time to see the future, please wait.',
                        'Building the Matrix. Please wait...',
                        'Creating transmutation circle...',
                        'Wait for it...']

    mod = sm.tsa.statespace.SARIMAX(Y,
                                    order = (p, d, q),
                                    exog=exog_variables,
                                    seasonal_order = (P, D, Q, s),
                                    enforce_invertibility=False
                                    )
    if quiet:
        try:
            results = mod.fit()
        except np.linalg.LinAlgError:
            mod = sm.tsa.statespace.SARIMAX(Y,
                                    order = (p, d, q),
                                    exog=exog_variables,
                                    seasonal_order = (P, D, Q, s),
                                    enforce_invertibility=False,
                                    initialization='approximate_diffuse'
                                    )
            results = mod.fit()

    else:
        with st.spinner(np.random.choice(waiting_messages)):
            try:
                results = mod.fit()
            except np.linalg.LinAlgError:
                mod = sm.tsa.statespace.SARIMAX(Y,
                                        order = (p, d, q),
                                        exog=exog_variables,
                                        seasonal_order = (P, D, Q, s),
                                        enforce_invertibility=False,
                                        initialization='approximate_diffuse'
                                        )
                results = mod.fit()
        st.success('Done!')
        
        try:
            st.text(results.summary())
        except:
            pass
    return results