How to use Alchemy
==================

Alchemy was built to be as intuitive as possible. It offers an interface that simulates the line of thinking of analysing and training a model for forecasting. This tutorial will guide you through all the process, starting by the top menus.

Your data menu
^^^^^^^^^^^^^^
.. image:: ../../img/alchemy_your_data_menu.gif

**This is where you will pick a file for Alchemy to analyse and model**. You can play with some toy datasets or you can `upload your own dataset <upload_data.html>`_ using the REST API. **You will also select the frequency of your data**. If your data was collected in a daily basis, select **Daily**, if it was collected in a monthly basis, select **Monthly**. This is an important step since **Alchemy will use this field to understand the seasonality of the time series**, and apply different techniques to find the best model.

**Fields**

- **Select a file**: an CSV, TXT, Excel, or delimited file. 
- **What is the FREQUENCY of your data?**: the frequency that the dataset was collected. Null values will be replaced by 0.

Choosing columns menu
^^^^^^^^^^^^^^^^^^^^^
.. image:: ../../img/alchemy_choosing_columns_menu.gif

This is step is composed by 4 fields that will instruct Alchemy which columns to use when training the model. In this step you can select **exogenous variables, what are nothing but columns that will help the model to give different ways for your predictions**. For example:

==========  =====  ===================
My Daily Sales
--------------------------------------
    Date    Sales  is_christmas_period
==========  =====  ===================
2019-11-29  500    0
2019-11-30  470    0
2019-12-01  200    1
2019-12-02  150    1
==========  =====  ===================

Let's say that you are predicting your company's daily sales, and in the Christmas period the sales go down. You can use a column called :code:`is_christmas_period`, where you place :code:`1` for rows (days) on your dataset that was collected in christmas period. Alchemy will try to use columns like this to enhance the predictions.

**Fields**

- **Which one is your DATE column?**: the column used to identify the time point where the data was collected.
- **Which column you want to PREDICT?**: the column with the values that you are trying to predict. It can be data like total sales, temperature measured, stock prices, and so on.
- **Which are your exogenous variables?**: the independent variables (e.g.: :code:`is_christmas_period`) that might be important to give different weights to predictions. **By informing exogenous variables will use automatically models that support regressors, e.g. ARIMAX.**
- **Validation set size**: how many period you want to let for Alchemy validate the model? **It's recommended to configure this field with the same amount of periods that you want to forecast**. For example, if your data was collected in a monthly basis, and you want to forecast the next 3 months, let this field with value 3.

Charts menu
^^^^^^^^^^^
.. image:: ../../img/alchemy_charts_menu.gif
In this section you can select some charts to appear on the screen. These charts are helpful to understand some steps of the model training, like the distribution data, seasonal decompose and out-of-sample predictions.

**Fields**

- **Historical data**: show the absolute distribution of your dataset just like it is. It can be useful to understand your data over time, and identify some interesting points like missing values of unusual scales.
- **Seasonal decompose**: show the components of your time series. It returns informations like the time series trending, seasonality, and resid (what remains when you remove trending and seasonality).
- **Dickey-Fuller statistical test**: to understand if your time series is stationary (one of the properties that make it possible to forecast data), Alchemy will execute the Augmented Dickey-Fuller test (a.k.a ADF test). By enabling this option, the transformed data with the best ADF test result (based on the lowest statistical result) will be plotted on Alchemy, with its moving average and standard deviation.
- **Train set predictions**: enable this option if you wanna check how your model is predicting the data that it was trained with. Two plots are placed in the figure, one for the observed (real) data (labeled as :code:`y`), and the predicted data (labeled as :code:`ŷ`).

Force data transformation menu
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Model parameters menu
^^^^^^^^^^^^^^^^^^^^^

Forecast periods menu
^^^^^^^^^^^^^^^^^^^^^