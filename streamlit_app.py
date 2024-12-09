import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

class COVIDDataExplorer:
    def __init__(self):
        # App configuration
        st.set_page_config(
            page_title="COVID-19 Global Insights",
            page_icon=":microbe:",
            layout="wide"
        )
        
        # Load and preprocess data
        self.load_data()
        
        # Custom CSS for professional look
        
    
    def load_data(self):
        """
        Load and preprocess COVID-19 data
        """
        @st.cache_data(ttl=24*3600)  # Cache data for 24 hours
        def fetch_covid_data():
            url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
            try:
                df = pd.read_csv(url)
                
                # Data preprocessing
                df['date'] = pd.to_datetime(df['date'])
                
                # Handle missing values
                columns_to_fill = [
                    'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 
                    'total_vaccinations', 'people_fully_vaccinated'
                ]
                for col in columns_to_fill:
                    df[col] = df[col].fillna(0)
                
                return df
            except Exception as e:
                st.error(f"Error loading data: {e}")
                return None
        
        self.df = fetch_covid_data()
        
        # Prepare filtered datasets
        if self.df is not None:
            # Latest data point for each country
            self.latest_data = self.df.groupby('location').last().reset_index()
            
            # Get list of countries
            self.countries = sorted(self.df['location'].unique())
    
    def global_overview(self):
        """
        Create comprehensive global COVID-19 overview
        """
        st.header("Global COVID-19 Snapshot")
        
        # Metrics columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Global Cases", 
                value=f"{self.latest_data['total_cases'].sum():,.0f}"
            )
        
        with col2:
            st.metric(
                label="Total Global Deaths", 
                value=f"{self.latest_data['total_deaths'].sum():,.0f}"
            )
        
        with col3:
            st.metric(
                label="Total Vaccinations", 
                value=f"{self.latest_data['total_vaccinations'].sum():,.0f}"
            )
        
        with col4:
            st.metric(
                label="Countries Affected", 
                value=f"{len(self.latest_data):,}"
            )
        
        # World map visualization
        st.subheader("Global Case Distribution")
        
        # Log transform for better visualization
        map_data = self.latest_data.copy()
        map_data['log_cases'] = np.log1p(map_data['total_cases'])
        
        fig = px.scatter_geo(
            map_data, 
            locations="location", 
            locationmode="country names",
            color="total_cases",
            size="log_cases",
            hover_name="location",
            hover_data={
                "total_cases": ":.0f",
                "total_deaths": ":.0f",
                "total_vaccinations": ":.0f"
            },
            color_continuous_scale="Viridis",
            title="COVID-19 Cases by Country"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def time_series_analysis(self):
        """
        Advanced time series analysis with multiple features
        """
        st.header("Time Series Analysis")
        
        # Sidebar for advanced filtering
        st.sidebar.header("Time Series Filters")
        
        # Country and metric selection
        selected_countries = st.sidebar.multiselect(
            "Select Countries", 
            self.countries, 
            default=["United States", "India", "Brazil"]
        )
        
        # Metrics selection
        metrics = st.sidebar.multiselect(
            "Select Metrics",
            ["new_cases", "total_cases", "new_deaths", "total_deaths", "new_vaccinations"],
            default=["new_cases", "new_deaths"]
        )
        
        # Date range selection
        date_range = st.sidebar.date_input(
            "Select Date Range", 
            [self.df['date'].min(), self.df['date'].max()]
        )
        
        # Convert date_range to datetime
        date_range = (pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))
        
        # Filter data
        filtered_df = self.df[
            (self.df['location'].isin(selected_countries)) &
            (self.df['date'].between(date_range[0], date_range[1]))
        ]
        
        # Plotting
        fig = px.line(
            filtered_df, 
            x="date", 
            y=metrics, 
            color="location",
            title="COVID-19 Metrics Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def predictive_modeling(self):
        """
        Simple predictive modeling for cases
        """
        st.header("Predictive Modeling")
        
        # Country selection for prediction
        predict_country = st.selectbox(
            "Select Country for Prediction", 
            self.countries
        )
        
        # Prepare data for prediction
        country_data = self.df[self.df['location'] == predict_country].copy()
        country_data['days_since_start'] = (country_data['date'] - country_data['date'].min()).dt.days
        
        # Prepare features and target
        X = country_data[['days_since_start']].values
        y = country_data['total_cases'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Model evaluation
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Visualization
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=X_test.flatten(), y=y_test, mode='markers', name='Actual'))
        fig.add_trace(go.Scatter(x=X_test.flatten(), y=y_pred, mode='lines', name='Predicted'))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Mean Squared Error", f"{mse:,.2f}")
        
        with col2:
            st.metric("R² Score", f"{r2:.2%}")
        
        st.plotly_chart(fig, use_container_width=True)
    
    def vaccination_progress(self):
        """
        Vaccination progress tracking
        """
        st.header("Vaccination Progress")
        
        # Top 10 countries by total vaccinations
        top_vaccination = self.latest_data.nlargest(10, 'total_vaccinations')
        
        fig = px.bar(
            top_vaccination, 
            x='location', 
            y='total_vaccinations',
            title='Top 10 Countries by Total Vaccinations'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Vaccination percentage
        top_vaccination['vaccination_percentage'] = (
            top_vaccination['people_fully_vaccinated'] / 
            top_vaccination['population'] * 100
        )
        
        # Percentage visualization
        fig_percentage = px.bar(
            top_vaccination, 
            x='location', 
            y='vaccination_percentage',
            title='Vaccination Percentage for Top 10 Countries'
        )
        st.plotly_chart(fig_percentage, use_container_width=True)
    
    def main(self):
        """
        Main Streamlit app runner
        """
        # Check if data is loaded
        if self.df is not None:
            # App sections
            self.global_overview()
            self.time_series_analysis()
            self.vaccination_progress()
            self.predictive_modeling()
        else:
            st.error("Unable to load COVID-19 data. Please check your connection.")

# Run the app
def main():
    explorer = COVIDDataExplorer()
    explorer.main()

if __name__ == "__main__":
    main()