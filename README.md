Project: Forecasts for Federal Reserve Bank of St. Louis
========================================================

The Federal Reserve Bank of St. Louis is having a labor crisis; everyone in
their forecasting group has taken off extended time for the holiday! Their
forecasting models are usually run ad-hoc by their analysts from their own PCs,
and the knowledge gap is wide enough, and the automation level low enough that
no one is available to generate forecasts for their public data. They have asked
us to help them throw together some rudimentary time-series forecasting software
using the tool of our choosing, and guide them towards a fully-automated
solution so that this never happens again.

Requirements:

- Demonstrate forecasting proof-of-concept by providing time-series forecasts
  for various public economic measures (starting with just one: `MONAN`, MO
  Total Non-Farm Employment, Thousands, Not Seasonally-Adjusted).

- No need for *intermediate* data persistence -- they have their own, obviously,
  which you'll be hitting via `GET` requests.

- Forecast results themselves should be stored in a database.

- Go above and beyond to demonstrate the power of clean, reliable automation by
  providing an extra feature along with the forecasts. This extra functionality
  can vary between tools, as long as it's valuable & unique.
