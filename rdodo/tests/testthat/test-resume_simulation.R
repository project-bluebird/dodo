require(testthat)
context("resume_simulation function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the resume_simulation function works", {

  aircraft_id <- "testResume"
  type <- "B744"
  latitude <- 0
  longitude <- 0
  heading <- 0
  flight_level <- 250
  speed <- 200

  expect_true(create_aircraft(aircraft_id = aircraft_id,
                              type = type,
                              latitude = latitude,
                              longitude = longitude,
                              heading = heading,
                              flight_level = flight_level,
                              speed = speed))

  # In the returned data frame aircraft_id is uppercase.
  aircraft_id <- toupper(aircraft_id)

  position0 <- aircraft_position(aircraft_id)

  expect_true(pause_simulation())

  position1 <- aircraft_position(aircraft_id)
  h_latitude <- config_param("latitude")

  # Check that the latitude increased since the first call to aircraft_position.
  expect_true(position1[aircraft_id, h_latitude] >
                position0[aircraft_id, h_latitude])

  # Check that the latitude has not changed since the last position call (as
  # the simulation was paused).
  position2 <- aircraft_position(aircraft_id)
  expect_identical(position1[aircraft_id, h_latitude],
                   position2[aircraft_id, h_latitude])

  expect_true(resume_simulation())

  # Check that the latitude increased since the simulation resumed.
  position3 <- aircraft_position(aircraft_id)
  expect_true(position3[aircraft_id, h_latitude] >
                position2[aircraft_id, h_latitude])
})
