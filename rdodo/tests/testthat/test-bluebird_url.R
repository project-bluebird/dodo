require(testthat)
context("bluebird_url function")

test_that("the bluebird_url function works", {

  scheme <- "http"
  stub <- paste(config::get("host"), config::get("port"), sep = ":")
  expected <- paste0(paste(scheme, stub, sep = "://"), "/")

  result <- bluebird_url()
  expect_identical(result, expected = expected)
})
