require(testthat)
context("bluebird_url function")

test_that("the bluebird_url function works", {

  scheme <- "http"
  stub <- paste(config_param("host"), config_param("port"), sep = ":")
  expected <- paste0(paste(scheme, stub, sep = "://"), "/")

  result <- bluebird_url()
  expect_identical(result, expected = expected)
})
