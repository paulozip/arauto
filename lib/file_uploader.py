import pandas as pd
import streamlit as st


def file_uploader(selected_file_format):
    """
    Read a CSV file uploaded to be used as a dataset for the model

    Args:
        selected_file_format (str): dropdown selection with file format
    Return:
        df (DataFrame): Pandas DataFrame with the dataset
    """
    # Avoid UnboundLocalError
    global df
    df = None

    if selected_file_format == "CSV or TXT":
        uploaded_file = st.sidebar.file_uploader("Choose a CSV or TXT file")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
            except pd._libs.parsers.ParserError:
                try:
                    df = pd.read_csv(uploaded_file, delimiter=";")
                except UnicodeDecodeError:
                    df = pd.read_csv(uploaded_file, delimiter=";", encoding="latin1")
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(uploaded_file, encoding="latin1")
                except pd._libs.parsers.ParserError:
                    df = pd.read_csv(uploaded_file, encoding="latin1", delimiter=";")
            except Exception as e:
                st.error(f"Error reading file: {e}")
    else:
        uploaded_file = st.sidebar.file_uploader("Choose an Excel file")
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
            except pd._libs.parsers.ParserError:
                try:
                    df = pd.read_excel(uploaded_file, delimiter=";")
                except UnicodeDecodeError:
                    df = pd.read_excel(uploaded_file, delimiter=";", encoding="latin1")
            except UnicodeDecodeError:
                try:
                    df = pd.read_excel(uploaded_file, encoding="latin1")
                except pd._libs.parsers.ParserError:
                    df = pd.read_excel(uploaded_file, encoding="latin1", delimiter=";")
            except Exception as e:
                st.error(f"Error reading file: {e}")

    if df is not None:
        if len(df) < 30:
            data_points_warning = """
                                The dataset contains too few data points to make a prediction. 
                                It is recommended to have at least 50 data points, but preferably 100 data points (Box and Tiao 1975).
                                This may lead to inaccurate predictions.
                                """
            st.warning(data_points_warning)
    return df
