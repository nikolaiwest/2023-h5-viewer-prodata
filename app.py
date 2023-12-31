import h5py
import streamlit as st
import plotly.graph_objects as go

# Project-specific module
from ui.auxiliaries import (
    labels_time_series,
    labels_single_metrics,
    labels_quality_metrics,
)


# Use streamlit's caching mechanism to avoid reloading the data for every rerun
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

    # Create a new Plotly figure object
    fig = go.Figure()
    legend = selected_metric

    # Get values
    data = []
    x_values = []

    # Count all errors (there errors occure due to machine handling)
    num_of_errors = 0 
    list_of_errors = []

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
            num_of_errors += 1
            list_of_errors += [cycle]
            continue

    if num_of_errors != 0:
        st.write(f"Total number of errors omitted: {num_of_errors}")
        st.write(list_of_errors)

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

    # Create a new Plotly figure object
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

    # Create a new Plotly figure object
    fig = go.Figure()
    legend = selected_metric

    # Get values
    data = []
    x_values = []

    # Control all errors
    num_of_errors = 0 
    list_of_errors = []

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
            num_of_errors += 1
            list_of_errors += [cycle]
            continue

    if num_of_errors != 0:
        st.write(f"Total number of errors omitted: {num_of_errors}")
        st.write(list_of_errors)

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
    # Data description
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total number of cycles:", value=len(list_of_cycles))
    col2.metric(label="Number of selected cycles:", value=len(selected_cycles))
    selection_ratio = round(len(selected_cycles) / len(list_of_cycles) * 100, ndigits=2)
    col3.metric(label="Ratio of selected cycles:", value=selection_ratio)

    # Header for visualizations
    st.sidebar.header("Select visalizations")
    st.header("Visualizations")

    # Sidebar single metrics
    st.sidebar.subheader("Single metrics")
    show_single_metrics = st.sidebar.checkbox(
        label="Show", value=True, key="show single metrics"
    )
    if show_single_metrics:
        single_metrics_to_select = list(labels_single_metrics.keys())
        selected_single_metrics = st.sidebar.multiselect(
            label="Select metrics to visualize",
            options=single_metrics_to_select,
            default=single_metrics_to_select[0],
            key="selected single metrics",
        )

        # Main page single metrics
        st.subheader("Single metric visualizations")

        # Iterate over selection
        for metric in selected_single_metrics:
            # plot each metric
            plot_single_metric(metric, selected_cycles, data)

    # Sidebar time series
    st.sidebar.subheader("Time series")
    show_time_series = st.sidebar.checkbox(
        label="Show", value=True, key="show time series"
    )
    if show_time_series:
        time_series_to_select = list(labels_time_series.keys())
        selected_time_series = st.sidebar.multiselect(
            label="Select metrics to visualize",
            options=time_series_to_select,
            default=time_series_to_select[1],
            key="selected time series",
        )

        # Main page time series
        st.subheader("Time series visualizations")

        # Iterate over selection
        for metric in selected_time_series:
            # plot each metric
            plot_time_series(metric, selected_cycles, data)

    # Sidebar quality metrics
    st.sidebar.subheader("Quality metrics")
    show_quality_metrics = st.sidebar.checkbox(
        label="Show", value=True, key="show quality metrics"
    )
    if show_quality_metrics:
        quality_metrics_to_select = list(labels_quality_metrics.keys())
        selected_quality_metrics = st.sidebar.multiselect(
            label="Select metrics to visualize",
            options=quality_metrics_to_select,
            default=quality_metrics_to_select[1],
            key="selected quality metrics",
        )

        # Main page quality metrics
        st.subheader("Quality metrics visualizations")

        # Iterate over selection
        for metric in selected_quality_metrics:
            # plot each metric
            plot_quality_metric(metric, selected_cycles, data)


except Exception as e:
    st.error(
        "The selected path is invalid. Please select a valid path to a H5 file from an\
            injection molding experiment.",
        icon="🚨",
    )
    st.write(e)
