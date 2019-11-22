Welcome to Alchemy's documentation! 
=======
.. image:: ../../img/logo.png
  :width: 600

| **Alchemy is an open-source and interactive tool for quick prototyping and experimentation of time series models**.
| You can use it to **build mixed autoregressive moving average models** (AR, MA, ARMA, ARIMA, SARIMA, ARIMAX, SARIMAX).

**Alchemy offers an intuitive experience**, so you can focus on the results of your model. Among other things, it supports exogenous variables and let you customize the whole process, from choosing a specific transformation function to test different parameters. Check it out the main features of Alchemy:

* **Support to exogenous regressors** (independent variables)
* Seasonal decompose that let's you know the **Trend, Seasonality and Resid** of your data
* Stationarity Test using **Augmented Dickey-Fuller** test
* Customization of data transforming for stationarity: you can use from first difference to seasonal log to transform your data
* **ACF** (Autocorrelation function) and **PACF** (Parcial correlation function) for terms estimation
* Customize ARIMA terms or **let Alchemy choose the best for you** based on your data
* **Grid search** feature for parameters tuning
* Code generation: at the end of the process, Alchemy returns the code used in the process

Contents
^^^^^^^^ 

.. toctree::
   :maxdepth: 2

   installation
   upload_data
   help