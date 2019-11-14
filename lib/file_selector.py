import os
import pandas as pd
import requests
import streamlit as st

from tkinter import Tk
from tkinter.filedialog import askopenfilename


def file_selector(folder_path='datasets/', ignore_upload=False):
    '''
    Selects a CSV file to be used as a dataset for the model

    Args:
        folder_path (str): the absolute path for the directory that contains datasets
        ignore_upload (bool): wether or not ignore the upload file. If True, the file dialog will not be shown
    Return:
        OS Path Directory
        df (DataFrame): Pandas DataFrame with the dataset
    '''
    if ignore_upload == False:
        root = Tk()
        root.withdraw() # we don't want a full GUI, so keep the root window from appearing

        session = requests.Session()
        
        filename = askopenfilename(master=root,
                                   initialdir=os.getcwd(), 
                                   title="Select file",
                                   filetypes=[("Delimited Files", "*.csv")]) # show an "Open" dialog box and return the path to the s
        files = {'file': open(filename, 'rb')}
        
        r = session.post('http://alchemy_api:5000/upload_file', files=files)

    filenames = os.listdir(folder_path)
    selected_filename = st.sidebar.selectbox('Select a file', filenames)
    df = pd.read_csv(os.path.join(folder_path, selected_filename))

    return os.path.join(folder_path, selected_filename), df