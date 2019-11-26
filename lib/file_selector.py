import os
import pandas as pd
import requests
import streamlit as st

def file_selector(folder_path='datasets/'):
    '''
    Selects a CSV file to be used as a dataset for the model

    Args:
        folder_path (str): the absolute path for the directory that contains datasets
    Return:
        OS Path Directory
        df (DataFrame): Pandas DataFrame with the dataset
    '''

    filenames = os.listdir(folder_path)
    filenames.sort()
    default_file_index = filenames.index('monthly_air_passengers.csv') if 'monthly_air_passengers.csv' in filenames else 0
    selected_filename = st.sidebar.selectbox('Select a file', filenames, default_file_index)
    
    # Checking if the file is in a valid delimited format
    if str.lower(selected_filename.split('.')[-1]) in ['csv', 'txt']:
        try:
            df = pd.read_csv(os.path.join(folder_path, selected_filename))
        except pd._libs.parsers.ParserError:
            try:
                df = pd.read_csv(os.path.join(folder_path, selected_filename), delimiter=';')
            except UnicodeDecodeError:
                df = pd.read_csv(os.path.join(folder_path, selected_filename), delimiter=';', encoding='latin1')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(os.path.join(folder_path, selected_filename), encoding='latin1')
            except pd._libs.parsers.ParserError:
                df = pd.read_csv(os.path.join(folder_path, selected_filename), encoding='latin1', delimiter=';')

    elif str.lower(selected_filename.split('.')[-1]) == 'xls' or str.lower(selected_filename.split('.')[-1]) == 'xlsx':
        try:
            df = pd.read_excel(os.path.join(folder_path, selected_filename))
        except pd._libs.parsers.ParserError:
            try:
                df = pd.read_excel(os.path.join(folder_path, selected_filename), delimiter=';')
            except UnicodeDecodeError:
                df = pd.read_excel(os.path.join(folder_path, selected_filename), delimiter=';', encoding='latin1')
        except UnicodeDecodeError:
            try:
                df = pd.read_excel(os.path.join(folder_path, selected_filename), encoding='latin1')
            except pd._libs.parsers.ParserError:
                df = pd.read_excel(os.path.join(folder_path, selected_filename), encoding='latin1', delimiter=';')
    else:
        st.error('This file format is not supported yet')

    if len(df) < 30:
        data_points_warning = '''
                              The dataset contains too few data points to make a prediction. 
                              It is recommended to have at least 50 data points, but preferably 100 data points (Box and Tiao 1975).
                              This may lead to inaccurate predictions.
                              '''
        st.warning(data_points_warning)
    return os.path.join(folder_path, selected_filename), df