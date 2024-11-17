import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joblib
import pickle

def predict():
    df = pd.read_csv('Traffic data.csv')
    df['Datetime'] = pd.to_datetime(df['Datetime'], format='%d-%m-%Y %H:%M')
    plt.figure(figsize=(10,7))
    plt.plot(df['Datetime'], df['Count'])
    plt.savefig("eda")
    df.index = df['Datetime']
    df['y'] = df['Count']
    df.drop(columns=['ID', 'Datetime', 'Count'], axis=1, inplace=True)
    df = df.resample('D').sum()
    df['ds'] = df.index
    loaded_model = joblib.load('prophet_model.joblib')
    future = loaded_model.make_future_dataframe(periods=60)
    forecast = loaded_model.predict(future)
    loaded_model.plot_components(forecast)
    pred = forecast.iloc[-60:, :]
    plt.savefig("forecast components")
    plt.figure(figsize=(10, 7))
    plt.plot(pred['ds'], pred['yhat'], color='red', label='Predicted')
    plt.fill_between(pred['ds'], pred['yhat_lower'], pred['yhat_upper'], color='orange', alpha=0.3, label='Uncertainty Interval')
    plt.xlabel('Date')
    plt.ylabel('Traffic Count')
    plt.title('Actual vs Predicted Traffic Count')
    plt.legend()
    plt.savefig("actual vs predicted")
    plt.plot(df['ds'], df['y'])
    plt.xlabel('Date')
    plt.ylabel('Traffic Count')
    plt.title('Traffic Data')
    plt.plot(forecast['ds'], forecast['yhat'])
    plt.xlabel('Date')
    plt.ylabel('Predicted Traffic Count')
    plt.title('Forecasted Traffic Count')
    