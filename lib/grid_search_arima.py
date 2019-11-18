import numpy as np
import statsmodels.api as sm
import streamlit as st

def grid_search_arima(train_data, exog,  p_range, q_range, P_range, Q_range, d=1, D=1, s=12):
    '''
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
        best_model_order (tuple): best model terms
    '''
    best_model_aic = np.Inf 
    best_model_bic = np.Inf 
    best_model_hqic = np.Inf
    best_model_order = (0, 0, 0)
    models = []
    with st.spinner('Finding best parameters. Please wait...'):
        for p_ in p_range:
            for q_ in q_range:
                for P_ in P_range:
                    for Q_ in Q_range:
                        try:
                            no_of_lower_metrics = 0
                            # Attention: the model is fitted with parameter enforce_invertibility set to False.
                            # The main reason is to avoid convergence problems. Your final model should be fitted with
                            # this parameter set to True
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
                                best_model_order = (p_, d, q_, P_, D, Q_, s)
                                current_best_model = model
                                resid = np.round(np.expm1(current_best_model.resid).mean(), 3)
                                models.append(model)
                                #st.markdown("------------------")
                                #st.markdown("**Best model so far**: SARIMA {}".format(best_model_order)) 
                                #st.markdown("**AIC**: {} **BIC**: {} **HQIC**: {} **Resid**: {}".format(best_model_aic, best_model_bic, best_model_hqic, resid))
                        except:
                            pass
    st.success('Grid Search done!')
    st.markdown('')
    st.markdown('### Best model results')
    st.text(current_best_model.summary())                
    #return current_best_model, models, best_model_order
    return best_model_order