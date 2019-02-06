library(stlfedR)

fred_id <- "MONAN"
saveRDS(fred_id, file.path(here::here(), "./fred_id.rds"))

# Read
df_0 <- get_FRED(fred_id, years_history = 5)

# Forecast
df_fcast <- make_fcast(df_0, fred_id, h = 12)

# Write to DB
db_write(df_fcast, fred_id, overwrite = TRUE)
