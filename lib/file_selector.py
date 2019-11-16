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
    selected_filename = st.sidebar.selectbox('Select a file', filenames)
    df = pd.read_csv(os.path.join(folder_path, selected_filename))

    return os.path.join(folder_path, selected_filename), df