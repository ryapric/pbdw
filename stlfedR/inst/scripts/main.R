library(forecast)
library(httr)
library(lubridate)
library(RSQLite)

url <- 'https://fred.stlouisfed.org/graph/fredgraph.csv'
fred_id <- 'MONAN' # MO Total Non-Farm Employment
today <- Sys.Date()
start_date <- today - years(5)
end_date <- today

# Shitty way around not asking for an API key
# Should eventually call httr::GET() with a key, to directly return a dataframe
tmpfile <- tempfile(fileext = '.csv')
download.file(glue::glue('{url}?id={fred_id}&cosd={start_date}&coed={end_date}'), tmpfile)

df_0 <- read.csv(tmpfile, strip.white = TRUE, stringsAsFactors = FALSE)

# Prep
df_0$DATE <- as_date(df_0$DATE)
df_0$label <- 'Actual'

# Fit HW model
ts_0 <- ts(
    df_0[, fred_id],
    start = c(year(min(df_0$DATE)), month(min(df_0$DATE))),
    end = c(year(max(df_0$DATE)), month(max(df_0$DATE))),
    frequency = 12
)
model <- ets(ts_0, model = 'ZZZ')

# Forecast
h <- 12
fcast <- forecast(model, h = h)

# Get MAPE
mape <- accuracy(fcast)[5]

first_fcast_period <- max(df_0$DATE) + months(1)
last_fcast_period <- max(df_0$DATE) + months(h)
fcast_dates <- seq(first_fcast_period, last_fcast_period, by = 'month')

df_fcast <- data.frame(
    DATE = fcast_dates,
    FRED_ID = as.numeric(fcast$mean),
    label = 'Forecast',
    MAPE = mape,
    stringsAsFactors = FALSE
)

# Can't easily parse names without metaprogramming, fuuuck that (for this example)
colnames(df_fcast)[which(colnames(df_fcast) == 'FRED_ID')] <- fred_id

# Build final output, and write to DB
df_out <- data.table::rbindlist(list(df_0, df_fcast), fill = TRUE)

con <- dbConnect(RSQLite::SQLite(), './fcast.db')
dbWriteTable(con, glue::glue('fcast_{fred_id}'), df_out, overwrite = TRUE)
dbDisconnect(con)

# Plot, for interactive use
plot(fcast)


# NOTE: This is some time saving bullshit to help with report generation later,
# which you can ignore for now
saveRDS(fred_id, file.path(here::here(), "./fred_id.rds"))
saveRDS(fcast, file.path(here::here(), "./fcast.rds"))
