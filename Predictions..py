#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np


# In[13]:



df = pd.read_csv(r"C:\Users\mayank\OneDrive\Desktop\Prediction\Lasalgaon.csv")

df['DATE'] = pd.to_datetime(df['DATE'], infer_datetime_format=True, dayfirst=True)

df = df.sort_values('DATE')

df.set_index('DATE', inplace=True)

print(df.head(5))


# In[39]:


plt.figure(figsize=(15,10))
plt.plot(df['Modal Price in KG'], label='Original Data', color='blue')
plt.title("Time Series Data (2 Years)")
plt.xlabel("Date")
plt.ylabel("Modal Price in KG")
plt.legend()
plt.show()


# In[40]:


train = df.iloc[:-30]
test = df.iloc[-30:]

# Naive forecast

naive_forecast = test.copy()
naive_forecast['Predicted'] = train['Modal Price in KG'].iloc[-1]  # simple version: last known value

naive_forecast['Predicted'] = test['Modal Price in KG'].shift(1)
naive_forecast.iloc[0, naive_forecast.columns.get_loc('Predicted')] = train['Modal Price in KG'].iloc[-1]


# In[16]:


plt.figure(figsize=(15,8))
plt.plot(train['Modal Price in KG'], label='Train Data')
plt.plot(test['Modal Price in KG'], label='Actual Test Data', color='blue')
plt.plot(naive_forecast['Predicted'], label='Naive Forecast', color='red', linestyle='--')
plt.title("Naïve Forecast Prediction")
plt.xlabel("Date")
plt.ylabel("Modal Price in KG")
plt.legend()
plt.show()


# In[17]:


mae = mean_absolute_error(test['Modal Price in KG'], naive_forecast['Predicted'])
rmse = np.sqrt(mean_squared_error(test['Modal Price in KG'], naive_forecast['Predicted']))

print("📉 Naïve Forecast Evaluation:")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")


# In[42]:


# Set Date as index (recommended for time series)
df_indexed = df.set_index('Date')
df_indexed.index = pd.to_datetime(df_indexed.index)

# Now this will work:
future_forecast = pd.DataFrame(index=pd.date_range(
    df_indexed.index[-1] + pd.Timedelta(days=1), 
    periods=15
))
future_forecast['Predicted'] = df_indexed['Modal Price in KG'].iloc[-1]

print(future_forecast)


# In[43]:



import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
import warnings
warnings.filterwarnings("ignore")

# Load and prepare data 
df = pd.read_csv(r"C:\Users\mayank\OneDrive\Desktop\Prediction\Lasalgaon.csv")
df['Date'] = pd.to_datetime(df['DATE'], dayfirst=True)
df.set_index('DATE', inplace=True)

# Plot actual prices 
plt.figure(figsize=(12,5))
plt.plot(df['Modal Price in KG'])
plt.title("Modal Price in KG")
plt.show()

# Stationarity test 
result = adfuller(df['Modal Price in KG'])
print('ADF Statistic:', result[0])
print('p-value:', result[1])

# --- SARIMA model ---
model = SARIMAX(df['Modal Price in KG'],
                order=(1,1,1),
                seasonal_order=(1,1,1,7),
                enforce_stationarity=False,
                enforce_invertibility=False)

sarima_result = model.fit()

# Forecast for 30 days 

df_indexed = df.set_index('Date')
df_indexed.index = pd.to_datetime(df_indexed.index)

future_forecast = pd.DataFrame(index=pd.date_range(
    df_indexed.index[-1] + pd.Timedelta(days=1), 
    periods=15
))
future_forecast['Predicted'] = df_indexed['Modal Price in KG'].iloc[-1]

print(future_forecast)
# Plot actual + forecast 
plt.figure(figsize=(12,5))
plt.plot(df['Modal Price in KG'], label='Actual')
plt.plot(forecast_df['mean'], label='Forecast', color='red')
plt.fill_between(forecast_df.index,
                 forecast_df['mean_ci_lower'],
                 forecast_df['mean_ci_upper'],
                 color='pink', alpha=0.3)
plt.legend()
plt.title("SARIMA Forecast for Next 30 Days")
plt.show()




# In[33]:


import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX


model = SARIMAX(df['Modal Price in KG'],
                order=(1,1,1),            
                seasonal_order=(1,1,1,7), 
                enforce_stationarity=False,
                enforce_invertibility=False)

sarima_result = model.fit()


forecast = sarima_result.get_forecast(steps=60)


# Set Date as index (recommended for time series)
df_indexed = df.set_index('Date')
df_indexed.index = pd.to_datetime(df_indexed.index)

future_forecast = pd.DataFrame(index=pd.date_range(
    df_indexed.index[-1] + pd.Timedelta(days=1), 
    periods=15
))
future_forecast['Predicted'] = df_indexed['Modal Price in KG'].iloc[-1]

print(future_forecast)

print(forecast_values)


# In[34]:


import pandas as pd
import matplotlib.pyplot as plt
import calendar
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings("ignore")

# Load your dataset 
df = pd.read_csv(r"C:\Users\mayank\OneDrive\Desktop\Prediction\Lasalgaon.csv")
df['DATE'] = pd.to_datetime(df['DATE'], dayfirst=True)
df = df.sort_values('DATE')

# Extract columns 
df['Year'] = df['DATE'].dt.year
df['Month_Num'] = df['DATE'].dt.month
df['Month'] = df['DATE'].dt.month_name()

# Build SARIMA model on full data
model = SARIMAX(df['Modal Price in KG'],
                order=(1,1,1),
                seasonal_order=(1,1,1,7),
                enforce_stationarity=False,
                enforce_invertibility=False)
sarima_result = model.fit()

# Forecast for next 90 days (Oct–Dec 2025) 
forecast_steps = 90
forecast = sarima_result.get_forecast(steps=forecast_steps)
forecast_mean = forecast.predicted_mean
forecast_dates = pd.date_range(start=df['DATE'].iloc[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq='D')

# Create forecast DataFrame
forecast_df = pd.DataFrame({'DATE': forecast_dates, 'Modal Price in KG': forecast_mean.values})
forecast_df['Year'] = forecast_df['DATE'].dt.year
forecast_df['Month_Num'] = forecast_df['DATE'].dt.month
forecast_df['Month'] = forecast_df['DATE'].dt.month_name()

# Monthly average for actual + forecast
monthly_actual = df.groupby(['Year', 'Month_Num', 'Month'])['Modal Price in KG'].mean().reset_index()
monthly_forecast = forecast_df.groupby(['Year', 'Month_Num', 'Month'])['Modal Price in KG'].mean().reset_index()

# Combine both
monthly_avg = pd.concat([monthly_actual, monthly_forecast], ignore_index=True)

# --- Pivot for plotting ---
pivot = monthly_avg.pivot(index='Year', columns='Month_Num', values='Modal Price in KG')
pivot = pivot.reindex(columns=list(range(1,13)))
month_labels = [calendar.month_name[m] for m in pivot.columns]

# setup
plt.figure(figsize=(14,5))

# Plot 2023–2024 normally
for year in pivot.index:
    if year not in [2025]:
        plt.plot(month_labels, pivot.loc[year], marker='o', linewidth=2, label=str(year))

# Plot 2025 (actual + SARIMA forecast)
if 2025 in pivot.index:
    y_values = pivot.loc[2025]

    past_months = list(range(1,10))   # Jan–Sep actual
    forecast_months = [10,11,12]      # Oct–Dec forecast

    past_values = y_values[past_months]
    forecast_values = y_values[forecast_months]

    # Actual till September (green)
    plt.plot([calendar.month_name[m] for m in past_months],
             past_values, color='green', marker='o', linewidth=2, label='2025 (Actual till Sep)')

    # SARIMA forecast (red)
    plt.plot([calendar.month_name[m] for m in forecast_months],
             forecast_values, color='red', marker='o', linestyle='--', linewidth=2, label='2025 (Forecast Oct–Dec)')


plt.title("Modal Price per Year (with Forecast for 2025)", fontsize=13)
plt.xlabel("Months")
plt.ylabel("Modal Price (₹ \ KG)")
plt.xticks(rotation=0)
plt.legend(title='Year', bbox_to_anchor=(1.02, 0.5), loc='center left')

plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x:.2f}/kg'))
plt.grid(False)
plt.tight_layout(rect=(0,0,0.85,1))


ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.show()


# In[ ]:




