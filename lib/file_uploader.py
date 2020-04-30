import io
import pandas as pd
import streamlit as st


def file_uploader(selected_file_format):
    """
    Read a CSV/TXT or Excel file uploaded to be used as a dataset for the model
    Args:
        selected_file_format (str): dropdown selection with file format
    Return:
        df (DataFrame): Pandas DataFrame with the dataset
    """
    df = None

    if selected_file_format == "CSV or TXT":
        uploaded_file = st.sidebar.file_uploader("Choose a CSV or TXT file")
        df = _csv_uploader(uploaded_file)
    elif selected_file_format == "Excel":
        uploaded_file = st.sidebar.file_uploader("Choose an Excel file")
        df = _excel_uploader(uploaded_file)

    if df is not None:
        _check_df_length(df)

    return df


@st.cache(show_spinner=False)
def _csv_uploader(uploaded_file):
    if uploaded_file is not None:
        file_contents = uploaded_file.getvalue()
        delimiter = _detect_delimiter(file_contents)
        try:
            df = pd.read_csv(uploaded_file, sep=delimiter)
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding="latin1")
        except Exception as e:
            st.error(f"Error reading file: {e}")

        return df


@st.cache(show_spinner=False)
def _excel_uploader(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error reading file: {e}")

        return df


def _check_df_length(df):
    if len(df) < 30:
        data_points_warning = """
                            The dataset contains too few data points to make a prediction. 
                            It is recommended to have at least 50 data points, but preferably 100 data points (Box and Tiao 1975).
                            This may lead to inaccurate predictions.
                            """
        st.warning(data_points_warning)


def _detect_delimiter(file_contents: str) -> str:
    """
    Reads the header of the file and naively detect what is the delimiter
    """
    file = io.StringIO(file_contents)
    header = file.readline()

    if header.find(";") != -1:
        return ";"
    if header.find(",") != -1:
        return ","
    if header.find("|") != -1:
        return "|"
    if header.find("¡") != -1:
        return "¡"

    return ";"
