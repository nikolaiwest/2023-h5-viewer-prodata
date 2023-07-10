# Injection Molding Data Viewer

This project aims to visualize data from an H5 file that was created in the process of running an injection molding machine. 
The application allows users to load H5 files, select cycles and metrics, and generate visualizations for single metrics, time series, and quality measurements. 
The visualizations are created using [Streamlit](https://docs.streamlit.io/library/api-reference), a python-based library to build and deploy web-apps.

## Installation

This project uses Python 3.11. It is recommended to use a virtual environment, such as Conda, to manage your Python environment and dependencies. Here's how to set it up:

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution) if you haven't already.

2. Open your terminal.

3. Create a new conda environment with ```Python``` and the required libraries:
    ```bash
    conda create --name myenv python h5py streamlit plotly 
    ```
4. Replace ```myenv``` with the name you want to give to your environment. Then, activate the environment with conda
    ```bash
    conda activate myenv
    ```

5. To avoid a import error, you have to reinstall ```streamlit``` when running the app for the first time
    ```bash
    pip install --upgrade streamlit
    ```
After these five steps, the environment is ready to run the H5 viewer.

## Usage 
To run the Streamlit app, navigate to the project folder, activate the environment and run the app like this: 
1. Activate the environment
    ``` bash
    conda activate myenv
    ```
2. Navigate to the project folder
    ``` bash
    cd path/to/the/repository
    ```
3. Run the streamlit interface
    ``` bash
    streamlit run app.py
    ```
A new tab in your default browser should open automatically. However, you an also access the interface manually using the local link [localhost:8501](localhost:8501).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.