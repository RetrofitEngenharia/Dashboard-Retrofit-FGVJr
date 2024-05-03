import io
import pandas as pd
import numpy as np
import datetime

def json_to_df(j):
    buffer = io.StringIO(j)
    processado = pd.read_json(buffer, orient="records")

    return processado


def df_to_json(df):
    return df.to_json(orient="records")

def apply_filter(df, filtro, groupby_columns=None):
    df_ = df.copy()  # Copy the dataframe to avoid modifying the original data
    date_column = "paymentDate" if "paymentDate" in df_.columns else "dueDate"

    # Convert date to string and ensure correct formatting as YYYYMM
    df_[date_column] = df_[date_column].astype(str).apply(lambda x: f"{x[:4]}{x[4:6]:0>2}")

    # Convert formatted strings to datetime objects for proper comparison
    df_[date_column] = pd.to_datetime(df_[date_column], format='%Y%m', errors='coerce')

    if filtro["projeto"] is not None:
        df_ = df_.loc[df_["projectId"] == filtro["projeto"]]
        
    # Filter based on the 'inicio' and 'fim' dates
    start_date = pd.to_datetime(filtro['inicio'], format='%Y-%m-%d', errors='coerce')
    end_date = pd.to_datetime(filtro['fim'], format='%Y-%m-%d', errors='coerce')
    df_ = df_.loc[(df_[date_column] >= start_date) & (df_[date_column] <= end_date)]

    if groupby_columns is not None:
        # Define aggregation methods for different types of columns
        aggregations = {col: 'sum' for col in df_.select_dtypes(include=[np.number]).columns}
        aggregations[date_column] = 'first'  # For datetime columns

        # Group by and aggregate without setting groupby columns as index
        df_ = df_.groupby(groupby_columns, as_index=False).agg(aggregations)

    return df_



