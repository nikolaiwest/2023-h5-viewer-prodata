# Import necessary libraries
import h5py
import streamlit as st
import plotly.graph_objects as go

# Project-specific module
# Contains constants for labels used in the project
from ui.auxiliaries import (
    labels_time_series,
    labels_single_metrics,
    labels_quality_metrics,
)

# Use streamlit's caching mechanism to avoid reloading the data for every rerun of the script
@st.cache_resource
def load_data(path: str) -> h5py.File:
    """
    Loads data from an h5 file.
    
    Parameters:
    path (str): The path to the h5 file.

    Returns:
    h5py.File: The loaded h5 file.
    """
    return h5py.File(path, "r+")

# Helper function to plot a single metric
def plot_single_metric(
    selected_metric: str, selected_cycles: list, imported_data: h5py.File
) -> None:
    """
    Creates a plot of a single metric.

    Parameters:
    selected_metric (str): The metric to be plotted.
    selected_cycles (list): The cycles for which the metric should be plotted.
    imported_data (h5py.File): The loaded h5 data file.
    """
    fig = go.Figure()
    legend = selected_metric

    data = []
    x_values = []

    # Loop over all cycles
    for cycle in selected_cycles:
        # Try to load the cycle data, if it fails due to KeyError (non-existing key),
        # skip the cycle and continue with the next one.
        try:
            data += [
                imported_data[
                    f"{cycle}/{labels_single_metrics[selected_metric]}_Value/block0_values"
                ][0][0]
            ]
            x_values += [imported_data[f"{cycle}/add_data/block3_values"][0][0]]
        except KeyError:
            st.write("key error")
            continue

    # Add data to figure
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=data,
            name=f"{legend} (all cycles)",
        )
    )

    # Configure plot layout
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(
        title=f"{legend}",
        xaxis_title="Observations",
        yaxis_title="Value",
        height=600,
        hovermode="x unified",
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)


# Helper function to plot a time series
def plot_time_series(
    selected_metric: str, selected_cycles: list, imported_data: h5py.File
) -> None:
    """
    Creates a plot of a time series value.

    Parameters:
    selected_metric (str): The metric to be plotted.
    selected_cycles (list): The cycles for which the metric should be plotted.
    imported_data (h5py.File): The loaded h5 data file.
    """
    fig = go.Figure()
    legend = selected_metric

    # Loop over all cycles
    for cycle in selected_cycles:
        # Get KurvenMesserwerte_i
        data_1 = imported_data[f"{cycle}/f3113I_Value/block0_values"][
            :, int(labels_time_series[selected_metric])
        ]
        # Get KurvenMesserwerte_ii
        data_2 = imported_data[f"{cycle}/f3213I_Value/block0_values"][
            :, int(labels_time_series[selected_metric])
        ]

        # Add data to figure
        fig.add_trace(
            go.Scatter(
                y=data_1 + data_2,
                mode="lines",
                name=f"{legend} ({cycle})",
            )
        )

    # Configure plot layout
    fig.update_layout(
        title=f"{legend}",
        xaxis_title="Time",
        yaxis_title="Value",
        height=600,
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)


# Helper function to plot a quality metric
def plot_quality_metric(
    selected_metric: str, selected_cycles: list, imported_data: h5py.File
) -> None:
    """
    Creates a plot of a quality metric.

    Parameters:
    selected_metric (str): The metric to be plotted.
    selected_cycles (list): The cycles for which the metric should be plotted.
    imported_data (h5py.File): The loaded h5 data file.
    """
    fig = go.Figure()
    legend = selected_metric

    data = []
    x_values = []

    # Loop over all cycles
    for cycle in selected_cycles:
        # Try to load the cycle data, if it fails due to KeyError (non-existing key),
        # skip the cycle and continue with the next one.
        try:
            data += [
                imported_data[f"{cycle}/add_data/block2_values"][0][
                    labels_quality_metrics[selected_metric]
                ]
            ]
            x_values += [imported_data[f"{cycle}/add_data/block3_values"][0][0]]
        except KeyError:
            st.write("key error")
            continue

    # Add data to figure
    fig.add_trace(
        go.Scatter(
            y=data,
            x=x_values,
            name=f"{legend} (all cycles)",
        )
    )

    # Configure plot layout
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(
        title=f"{legend}",
        xaxis_title="Observations",
        yaxis_title="Value",
        height=600,
        hovermode="x unified",
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)


# Configure the layout of the Streamlit app
st.set_page_config(layout="wide")

# Headers configuration for the side bar
st.sidebar.title("Settings")

# Main page configuration
st.title("Injection Molding Data Viewer")
st.write("This application allows you to visualize time series data from an H5 file.")

# Header for data loading section
st.sidebar.header("Load data")

# User input for the file path
path = st.sidebar.text_input("Path to file:", "data/20230704.h5")

# Load data from the H5 file and continue
try:
    # Get data from h5 file
    data = load_data(path)
    list_of_cycles = list(data.keys())

    # Header for observations / selected data
    st.sidebar.header("Select observations")
    st.header("Data description")

    # User input for selecting cycles
    select_all_cylces = st.sidebar.checkbox("Select all cylces")
    if select_all_cylces:
        selected_cycles = list_of_cycles
    else:
        selected_cycles = st.sidebar.multiselect(
            "Select one or more cycles:", options=list_of_cycles
        )
    col1, col2, col3 = st.columns(3)
    # User input for selecting a single metric
    with col1:
        st.header("Single Metrics")
        single_metric = st.selectbox(
            "Select a single metric:",
            options=list(labels_single_metrics.keys()),
            key="single_metric",
        )
        plot_single_metric(single_metric, selected_cycles, data)

    # User input for selecting a time series metric
    with col2:
        st.header("Time Series")
        time_series_metric = st.selectbox(
            "Select a time series metric:",
            options=list(labels_time_series.keys()),
            key="time_series",
        )
        plot_time_series(time_series_metric, selected_cycles, data)

    # User input for selecting a quality metric
    with col3:
        st.header("Quality Metrics")
        quality_metric = st.selectbox(
            "Select a quality metric:",
            options=list(labels_quality_metrics.keys()),
            key="quality_metric",
        )
        plot_quality_metric(quality_metric, selected_cycles, data)
except OSError:
    st.sidebar.warning("Please input a valid h5 file path.")
    st.sidebar.text_input("Path to file:", value="", key="file_path")
