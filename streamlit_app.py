import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np

class COVIDExplorer:
    def __init__(self):
        self.load_data()
    
    def load_data(self):
        """
        Load COVID-19 data from Our World in Data
        """
        url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
        try:
            self.df = pd.read_csv(url)
            
            # Data preprocessing
            self.df['date'] = pd.to_datetime(self.df['date'])
            
            # Latest data point for each country, removing NaNs
            self.latest_data = self.df.groupby('location').last().reset_index()
            self.latest_data = self.latest_data.dropna(subset=['total_cases'])
            
            self.countries = sorted(self.latest_data['location'].unique())
        except Exception as e:
            st.error(f"Error loading data: {e}")
            self.df = None
    
    def global_overview(self):
        """
        Create global COVID-19 overview visualization
        """
        st.header("Global COVID-19 Overview")
        
        # Ensure we have numerical values for size
        size_column = np.log1p(self.latest_data['total_cases'])
        
        # World map of total cases
        fig = px.scatter_geo(
            self.latest_data, 
            locations="location", 
            locationmode="country names",
            color="total_cases",
            size=size_column,
            hover_name="location",
            hover_data={
                "location": True, 
                "total_cases": ":.0f",
                "total_vaccinations": ":.0f"
            },
            color_continuous_scale="Viridis",
            title="Total Confirmed COVID-19 Cases by Country"
        )
        st.plotly_chart(fig)
    
    def time_series_analysis(self):
        """
        Time series analysis of COVID-19 cases
        """
        st.header("Time Series Analysis")
        
        # Country selection
        selected_countries = st.multiselect(
            "Select Countries", 
            self.countries, 
            default=["United States", "India", "Brazil"]
        )
        
        # Metric selection
        metric = st.selectbox(
            "Select Metric", 
            ["new_cases", "total_cases", "new_vaccinations"]
        )
        
        # Filter and plot
        filtered_df = self.df[self.df['location'].isin(selected_countries)]
        
        fig = px.line(
            filtered_df, 
            x="date", 
            y=metric, 
            color="location",
            title=f"{metric.replace('_', ' ').title()} Over Time"
        )
        st.plotly_chart(fig)
    
    def main(self):
        """
        Main Streamlit app
        """
        st.title("Interactive COVID-19 Data Explorer")
        
        if self.df is not None:
            self.global_overview()
            self.time_series_analysis()
        else:
            st.error("Unable to load COVID-19 data. Please check your connection.")

# Run the app
if __name__ == "__main__":
    explorer = COVIDExplorer()
    explorer.main()