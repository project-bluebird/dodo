require(testthat)
context("position_call function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the position_call function works with invalid aircraft ID", {

  # Missing aircraft_id (i.e. not found in the simulation).
  invalid_id <- "NoSuchAircraft"

  # Expect an empty list.
  expect_identical(position_call(invalid_id), expected = list())
})

# TODO: add tests with a valid aircraft ID.
