import requests
import datetime
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt

# Shitty way around not asking for an API key, since returned data is raw text
url = 'https://fred.stlouisfed.org/graph/fredgraph.csv'
fred_id = 'MONAN' # MO Total Non-Farm Employment
today = datetime.datetime.now().strftime('%Y-%m-%d')
start_date = (pd.to_datetime(today) - pd.DateOffset(years = 5)).strftime('%Y-%m-%d')
end_date = today
r = requests.get(f'{url}?id={fred_id}&cosd={start_date}&coed={end_date}')

with open('fred_id.csv', 'w') as f:
    f.write(r.text)

df = pd.read_csv('fred_id.csv')

# Prep
df['DATE'] = pd.to_datetime(df['DATE'])
df['label'] = 'Actual'

# I don't know if I actually need this
# df.index.freq = 'MS'

# Fit HW model
model = ExponentialSmoothing(
    df[fred_id],
    trend = 'add',
    seasonal = 'add',
    seasonal_periods = 12
).fit()

# Get MAPE
pct_error = np.abs(df[fred_id] - model.fcastvalues) / df[fred_id]
mape = np.mean(pct_error) * 100

# Forecast
h = 12
fcast = model.forecast(h)
# Jesus, this is messy
df_fcast = pd.DataFrame(
    data = {
        'DATE': pd.date_range(pd.to_datetime(df['DATE'].values[len(df.index)-1]) + pd.DateOffset(months = 1), periods = h, freq = 'MS'),
        fred_id: fcast,
        'label': 'Forecast',
        'MAPE': mape
    }
)

# Plotting, just for interactive use
plt.plot(df['DATE'], df[fred_id], label = 'Actual')
plt.plot(df_fcast['DATE'], df_fcast[fred_id], label = 'Forecast')
plt.legend(loc = 'best')
plt.show()
