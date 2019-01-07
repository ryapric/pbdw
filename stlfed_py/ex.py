import requests
import datetime
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt

# Shitty way around not asking for an API key, since returned data is raw text
url = 'https://fred.stlouisfed.org/graph/fredgraph.csv'
fred_id = 'MONAN' # MO Total Non-Farm Employment
start_date = '1800-01-01'
today = datetime.datetime.now().strftime('%Y-%m-%d')
end_date = today
r = requests.get(f'{url}?id={fred_id}&cosd={start_date}&coed={end_date}')

with open('fred_id.csv', 'w') as f:
    f.write(r.text)

df = pd.read_csv('fred_id.csv')
df[fred_id] = (df[fred_id] / 100)

df.index.freq = 'M'

# Fit HW model
model = ExponentialSmoothing(
    df[fred_id],
    trend = 'add',
    seasonal = 'add',
    seasonal_periods = 12
).fit()

# Get MAPE
pct_error = abs(df[fred_id] - model.fittedvalues) / df[fred_id]
mape = np.mean(pct_error)

# Forecast
h = 12
fcast = model.forecast(h)

# Full series
out = df[fred_id].append(fcast)

# Plotting, just for interactive use
plt.plot(df.index, df[fred_id], label = 'Actual')
plt.plot(range(len(df.index), len(df.index) + h), fcast, label = 'Fcast')
plt.legend(loc = 'best')
plt.show()
