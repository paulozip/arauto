[![Documentation Status](https://readthedocs.org/projects/arauto/badge/?version=latest)](https://arauto.readthedocs.io/en/latest/?badge=latest)
![](https://img.shields.io/github/languages/top/paulozip/arauto)
![](https://img.shields.io/github/issues-raw/paulozip/arauto?color=%4cd137)
![](https://img.shields.io/github/issues-closed/paulozip/arauto?color=%238e44ad)

![](img/logo.png)
# Arauto
*A interactive tool for time series experimentation and forecasting*

Arauto is an open-source framework that aims to make it **easier to model and experiment time series analysis and forecasting**. Arauto offers a intuitive and interactive interface to explore different parameters for models using Autoregressive models (AR, ARMA, ARIMA, SARIMA, ARIMAX, and SARIMAX). More estimators and algorithms are on the way.

## Features

* **Support for exogenous regressors** (independent variables)
* Seasonal decompose that lets you know the **Trend, Seasonality, and Resid** of your data
* Stationarity Test using **Augmented Dickey-Fuller** test
* Customization of data transforming for stationarity: you can use from first difference to seasonal log to transform your data
* **ACF** (Autocorrelation function) and **PACF** (Parcial correlation function) for terms estimation
* Customize ARIMA terms or **let Arauto choose the best for you** based on your data
* **Grid search** feature for parameters tuning
* Code generation: at the end of the process, Arauto returns the code used to transform the data and train the model

# Getting started
Arauto can be used in three different ways:

## Web
If you are just curious about what you can do with Arauto, **[you can refer to this website](https://projectarauto.herokuapp.com)**. This version contains some toy datasets that you can use to check how Arauto works. 

**IMPORTANT: please be aware that this web version is a lightweight version of Arauto, with low computational power and with some features disable, since we are using a free-tier version of Heroku instance.**. To understand the full potential of Arauto, use one of the installations version below.

## Docker
Run the following commands to use Arauto with Docker (requires **Docker and Docker-compose**):

```bash
# Run the docker compose
docker-compose up --build
```

## Local installation (requirements.txt)
**Tip**: we recommend you to use Anaconda environments

```bash
# Clone the repository
git clone https://github.com/paulozip/arauto.git
cd arauto

# If you're using Anaconda
conda create --name arauto_env
conda activate arauto_env

# Install dependencies
pip install requirements.txt

# Run Streamlit
streamlit run run.py
```

# How to use
[Please refer to our documentation](https://arauto.readthedocs.io/en/latest/how_to_use.html) to check the tutorial that we prepared to help you to build your own models.

# Upload your data
A [Upload file support will be added to Arauto](https://github.com/paulozip/arauto/issues/4), but you can use the Arauto REST API to send your dataset. Here's an example of how you can use it using cURL:

```bash
curl -X POST \
  http://SERVER_ADDRESS:5000/upload_file \
  -H 'content-type: multipart/form-data' \       
  -F file=@PATH_TO_YOUR_FILE
```

Example:
```bash
curl -X POST \
  http://0.0.0.0:5000/upload_file \
  -H 'content-type: multipart/form-data' \       
  -F file=@/home/my_user/Downloads/dataset.csv
```

# Your data, your code
At the end of the process, Arauto will give you the source code used to make the exploration and training. Use this code to adapt your work and make modifications at will. **PROTIP: Arauto is also a useful tool to generate boilerplate code for time series**.

![](img/arauto_your_code.png)

# Next steps
Currently, this is an one-person project, but help is always welcome. **[You can suggest new ideas and features for us in our issue tracking](https://github.com/paulozip/arauto/issues). Requests will be prioritized by thumbs up emoji** (👍).

**If you want to collaborate with this project**, all you need to do is fork this repository, make new additions and modifications, and open a PR. I will validate it ASAP. 

# Get updated
New features will be added to Arauto. If you want to know when a new version arrives, please, **[subscribe to Arauto’s newsletter to get informed about new things](https://6f9c43ce.sibforms.com/serve/MUIEAI8Dq-U5iguZoH4tTXCgd1XsWZ2kDTwXG61HzqOe1smcmeFu1AKhca2lt0WmMOTwn3lGTx9zN1pk-0eo795pAFuq4eWzfH7edyG4Tk6tUsSq6vAwQdYlowk0MDXBSoDKIdsnzjRs_H_i8sjz2rRJDmtjRIW_xUmkUh03sW4qvUf7iaP1sMAlu1fAZ4XkZOi7I6562dzbkFn8)**. We will NOT send spams or share your email. Only content related to Arauto will be sent.

# A big thank you
This project would not be possible without [Streamlit](https://github.com/streamlit/streamlit): an awesome tool to build ML tools. Please refer to their Github repository to know further, or you can also [check their blog post](https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace)
