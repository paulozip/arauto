import plotly.graph_objs as go
import streamlit as st

def plot_forecasts(forecasts, confidence_interval, periods):
    '''
    Generate a plot with the forecasted observations

    Args.
        forecasts (Pandas Series): out-of-sample observations
        confidence_interval (Pandas DataFrame): DataFrame containing a column for the lower boundary and another for the upper boundary 
        periods (int): how much periods to forecast?
    '''
    lower_ci = {"x": confidence_interval.index, 
                "y": confidence_interval['ci_lower'], 
                "line": {
                    "color": "#1EBC61", 
                    "shape": "linear",
                    "width": 0.1
                        }, 
                "mode": "lines",
                "name": "Lower 95% CI", 
                "showlegend": False, 
                "type": "scatter", 
                "xaxis": "x", 
                "yaxis": "y"
                }
    upper_ci = {"x": confidence_interval.index, 
                "y": confidence_interval['ci_upper'], 
                "fill": "tonexty", 
                "line": {
                    "color": "#1EBC61", 
                    "shape": "linear",#"spline",
                    "width": 0.1
                        }, 
                "mode": "lines", 
                "name": "Upper 95% CI", 
                "type": "scatter", 
                "xaxis": "x", 
                "yaxis": "y"
                }
    forecasting =  {'x': forecasts.index, 
                    'y': forecasts.values,
                    "line": {
                            "color": "#005C01", 
                            "shape": "linear",
                            "width": 3
                            }, 
                    "mode": "lines", 
                    "name": "Forecasting", 
                    "type": "scatter", 
                    "xaxis": "x", 
                    "yaxis": "y"                }

    plot_data = ([lower_ci, upper_ci, forecasting])
    layout = go.Layout(title = f'{periods} Forecasts')
    fig = go.Figure(data = plot_data, layout=layout)
    st.plotly_chart(fig)