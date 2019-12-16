require(testthat)
context("simulation_time function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the simulation_time function works", {

  result <- simulation_time()
  expect_true(inherits(result, "POSIXct"))
})
