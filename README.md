# COVID-19 Data Explorer

## Overview

The COVID-19 Data Explorer is a Streamlit-based web application that provides comprehensive insights into the global COVID-19 pandemic. The app allows users to explore COVID-19 data, perform time series analysis, and create predictive models for various countries.

## Features

- **Global Overview**: Visualize the latest COVID-19 statistics for different countries.
- **Time Series Analysis**: Analyze COVID-19 metrics over time with advanced filtering options.
- **Predictive Modeling**: Create simple predictive models for COVID-19 cases using linear regression.

## Installation

To run the COVID-19 Data Explorer locally, follow these steps:

1. **Clone the repository**:

    ```sh
    git clone https://github.com/yourusername/COVID-19-Data-Explorer.git
    cd COVID-19-Data-Explorer
    ```

2. **Create a virtual environment**:

    ```sh
    python -m venv env
    ```

3. **Activate the virtual environment**:
    - On Windows:

        ```sh
        .\env\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source env/bin/activate
        ```

4. **Install the required packages**:

    ```sh
    pip install -r requirements.txt
    ```

5. **Run the Streamlit app**:

    ```sh
    streamlit run streamlit_app.py
    ```

## Usage

Once the app is running, you can access it in your web browser. The app provides several functionalities:

- **Global Overview**: View the latest COVID-19 statistics for different countries.
- **Time Series Analysis**: Use the sidebar to select countries, metrics, and date ranges for analysis. The app will display a line chart of the selected metrics over time.
- **Predictive Modeling**: Select a country for prediction, and the app will create a simple linear regression model to predict future COVID-19 cases.

## Data Source

The COVID-19 data used in this app is sourced from the [Our World in Data](https://github.com/owid/covid-19-data) repository.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please create a pull request or open an issue.

## License

This project is licensed under the Apache-2.0 license.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/)
- [Scikit-learn](https://scikit-learn.org/)
- [Our World in Data](https://ourworldindata.org/)
