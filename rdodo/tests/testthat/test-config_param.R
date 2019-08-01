require(testthat)
context("config_param function")

test_that("the config_param function works", {

  result <- config_param("port")

  expect_true(is.character(result))
  expect_true(nchar(result) == 4)
})

test_that("the config_param function throws an error if the param is not found", {

  expect_error(config_param("poxt"), regexp = "not found")
})
