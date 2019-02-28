require(testthat)
context("aircraft_position function")

test_that("the config_param function works", {

  result <- config_param("port")

  expect_true(is.character(result))
  expect_true(nchar(result) == 4)
})
