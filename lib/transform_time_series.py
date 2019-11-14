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
    df.index = df.index.astype('datetime64[ns]')

    return df