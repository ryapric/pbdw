#' Get FRED Data into DF
#' 
#' See title
#'
#' @param fred_id ID for FRED data ticker
#' @param years_history NUmber of hostoirial years of data to grab who car about splenbign
#' @export
get_FRED <- function(fred_id, years_history) {
    url <- 'https://fred.stlouisfed.org/graph/fredgraph.csv'
    today <- Sys.Date()
    start_date <- today - years(years_history)
    end_date <- today
    
    # Shitty way around not asking for an API key
    # Should eventually call httr::GET() with a key, to directly return a dataframe
    tmpfile <- tempfile(fileext = '.csv')
    download.file(glue::glue('{url}?id={fred_id}&cosd={start_date}&coed={end_date}'), tmpfile)
    
    df_0 <- read.csv(tmpfile, strip.white = TRUE, stringsAsFactors = FALSE)
    df_0$DATE <- as_date(df_0$DATE)
    df_0$label <- 'Actual'
    
    return(df_0)
}
