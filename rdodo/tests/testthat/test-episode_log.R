require(testthat)
context("episode_log function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

test_that("the episode_log function works", {

  # Reset the simulation.
  reset_simulation()

  # Create & load a test scenario.
  filename <- system.file("dodo-test-scenario.scn", package = "rdodo")
  scenario <- "dodo-test-scenario"
  expect_true(create_scenario(filename, scenario))
  expect_true(load_scenario(scenario))

  # Save the episode log file to the rdodo package installation directory.
  path <- system.file(package = "rdodo")
  result <- episode_log(path)

  # Check that the downloaded log file exists.
  expect_true(file.exists(result))
  expect_true(file.size(result) > 0)

  # Tidy up.
  logs_dir <- file.path(path, "logs")
  if (dir.exists(logs_dir))
    unlink(logs_dir, recursive = TRUE)
})
