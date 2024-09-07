import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet

def load_data(file_path, file_format='csv'):
    """Load data from an Excel or CSV file."""
    if file_format == 'csv':
        return pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
    else:
        raise ValueError("Unsupported file format")

def plot_arima(df):
    """Plot ARIMA forecast."""
    arima_model = ARIMA(df['Sales'], order=(5, 1, 0))
    arima_model_fit = arima_model.fit()
    arima_forecast = arima_model_fit.forecast(steps=10)
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['Sales'], label='Original Sales')
    plt.plot(pd.date_range(start=df.index[-1], periods=10, freq='D'), arima_forecast, label='ARIMA Forecast', color='red')
    plt.title('Sales Forecast using ARIMA')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.grid(True)
    plt.savefig('images/arima_forecast.png')
    plt.show()

def plot_prophet(df):
    """Plot Prophet forecast."""
    df_prophet = df.reset_index().rename(columns={'Date': 'ds', 'Sales': 'y'})
    prophet_model = Prophet()
    prophet_model.fit(df_prophet)
    future = prophet_model.make_future_dataframe(periods=10)
    forecast = prophet_model.predict(future)
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['Sales'], label='Original Sales')
    plt.plot(forecast['ds'], forecast['yhat'], label='Prophet Forecast', color='green')
    plt.title('Sales Forecast using Prophet')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.grid(True)
    plt.savefig('images/prophet_forecast.png')
    plt.show()

def main():
    # File path to the data file
    file_path = 'data/sales_data.csv'
    
    # Load data
    df = load_data(file_path)
    
    # Plot forecasts
    plot_arima(df)
    plot_prophet(df)
    
    print("Data processing complete. Results saved to 'images/arima_forecast.png' and 'images/prophet_forecast.png'.")

if __name__ == "__main__":
    main()

