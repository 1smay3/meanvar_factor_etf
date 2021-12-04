import plotly.express as px
import pandas as pd#


def line_chart(dataframe : pd.DataFrame, x_col_name: str, y_col_name: str, title:str):
    fig = px.line(dataframe, x=x_col_name, y=y_col_name, title=title)
    return fig