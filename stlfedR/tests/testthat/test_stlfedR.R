library(testthat)

context("Readers")

test_that("get_FRED gets FRED Data (duh).", {
    df_0 <- get_FRED("MONAN", years_history = 1)
    expect_true("data.frame" %in% class(df_0))
})

context("Forcasters")

test_that("Forecasts work", {
    df_0 <- get_FRED("MONAN", years_history = 5)
    df_fcast <- make_fcast(df_0, "MONAN", 12)
    expect_true(nrow(df_0) + 12 == nrow(df_fcast))
    # expect_true()
    
    df_fcast <- make_fcast(df_0, "MONAN", 6)
    expect_true(nrow(df_0) + 6 == nrow(df_fcast))
})

context("Writers")

test_that("DB writes happen", {
    df_0 <- get_FRED("MONAN", years_history = 5)
    df_fcast <- make_fcast(df_0, "MONAN", 12)
    db_write(df_fcast, "MONAN", overwrite = TRUE)
    df_in_db <- DBI::dbReadTable()
    expect_equal()
})

test_that("Forcasts go to S3", {
    
})
