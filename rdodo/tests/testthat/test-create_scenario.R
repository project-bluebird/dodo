require(testthat)
context("create_scenario function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the create_scenario function works", {

  filename <- system.file("dodo-test-scenario.scn", package = "rdodo")

  # Check for an error on attempt to create a scenario without a name.
  expect_error(create_scenario(filename))
})

test_that("the create_scenario function works", {

  # Check that the aircraft in the test scenario do not yet exist.
  aircraft_ids <- rownames(all_positions())
  expect_true(length(aircraft_ids) == 0)

  filename <- system.file("dodo-test-scenario.scn", package = "rdodo")
  scenario <- "dodo-test-scenario"
  expect_true(create_scenario(filename, scenario))

  Sys.sleep(0.1)

  # Load the newly-created scenario.
  expect_true(load_scenario(scenario))

  Sys.sleep(0.5)

  # Check that the aircraft created in the test scenario exist.
  aircraft_ids <- rownames(all_positions())
  expect_false(length(aircraft_ids) == 0)
  expect_true(all(c("TST1001", "TST2002") %in% aircraft_ids))
})
