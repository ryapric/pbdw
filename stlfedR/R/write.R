#' Title
#'
#' @param df_0 
#' @param fred_id 
#' @param ... 
#' @export
db_write <- function(df_0, fred_id, ...) {
    con <- dbConnect(RSQLite::SQLite(), './fcast.db')
    dbWriteTable(con, glue::glue('fcast_{fred_id}'), df_0, ...)
    dbDisconnect(con)
}
