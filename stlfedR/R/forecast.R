#' Title
#'
#' @param df_0 
#' @param fred_id 
#' @export
make_fcast <- function(df_0, fred_id, h = 12) {
    ts_0 <- ts(
        df_0[, fred_id],
        start = c(year(min(df_0$DATE)), month(min(df_0$DATE))),
        end = c(year(max(df_0$DATE)), month(max(df_0$DATE))),
        frequency = 12
    )
    model <- ets(ts_0, model = 'ZZZ')
    
    # Forecast
    fcast <- forecast(model, h = h)
    saveRDS(fcast, file.path(here::here(), "./fcast.rds"))
    
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
    
    df_out
}
