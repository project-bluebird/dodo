require(testthat)
context("aircraft_position function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

test_that("the reset_simulation function works", {
  expect_true(reset_simulation())
})
