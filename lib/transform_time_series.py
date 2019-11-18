import pandas as pd

def transform_time_series(df, ds_column):
    '''
    Transforms a Pandas DataFrame into a Pandas Series, using a column as the index

    Args:
        df (Pandas DataFrame): a DataFrame to be transformed
        ds_column (str): column name that will be used as an index

    Return:
        df (Pandas Series): transformed DataFrame
    '''
    df.set_index(ds_column, inplace = True)

    try:
        df.index = df.index.astype('datetime64[ns]')
        df = df.dropna()
    except TypeError:
        error_message = '''
                        There was a problem while we tried to convert the DATE column for a valid format.
                        Be sure there is no null value in the DATE column and that it is in a valid format for Pandas to_datetime function.
                        '''
        raise TypeError(error_message)
    return df