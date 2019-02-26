require(testthat)
context("all_positions function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the all_positions function works when no aircraft exist", {

  result <- all_positions()

  # Expect an empty data frame.
  expect_true(is.data.frame(result))
  expect_identical(object = nrow(result), expected = 0L)
  expected <- c("altitude", "ground_speed", "latitude", "longitude", "vertical_speed")
  expect_identical(object = colnames(result), expected = expected)
})

# TODO: test when aircraft exist!
