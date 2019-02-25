require(testthat)
context("construct_endpoint_url function")

test_that("the construct_endpoint_url function works", {

  endpoint <- "abc"
  result <- construct_endpoint_url(endpoint = endpoint)

  scheme <- "http"
  stub <- paste(config::get("host"), config::get("port"), sep = ":")
  url <- paste(stub, config::get("api_path"), config::get("api_version"),
               endpoint, sep = "/")
  expected <- paste(scheme, url, sep = "://")

  expect_identical(result, expected = expected)

  # Test with a non-null query argument.
  query <- list("acid" = "BA456")

  result <- construct_endpoint_url(endpoint = endpoint, query = query)
  expected <- paste(expected, paste(names(query), query, sep = "="), sep = "?")
  expect_identical(result, expected = expected)
})
