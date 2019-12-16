require(testthat)
context("change_vertical_speed function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the change_vertical_speed function works", {

  aircraft_id <- "test-change-vertical-speed"
  type <- "B744"
  latitude <- 0
  longitude <- 0
  heading <- 0
  flight_level <- 250
  speed <- 265

  # Create an aircraft.
  expect_true(create_aircraft(aircraft_id = aircraft_id,
                              type = type,
                              latitude = latitude,
                              longitude = longitude,
                              heading = heading,
                              flight_level = flight_level,
                              speed = speed))

  # In the returned data frame aircraft_id is uppercase.
  aircraft_id <- toupper(aircraft_id)

  # Check the vertical speed.
  position <- aircraft_position(aircraft_id)
  h_vspeed <- config_param("vertical_speed")

  expect_equal(position[aircraft_id, h_vspeed], expected = 0)

  # Give the command to ascend.
  new_flight_level <- 450
  expect_true(change_altitude(aircraft_id = aircraft_id,
                              flight_level = new_flight_level))

  # Test with an invalid vertical speed.
  invalid_vertical_speed <- -1
  expect_error(change_vertical_speed(aircraft_id = aircraft_id,
                            vertical_speed = invalid_vertical_speed))

  # Test with an invalid units.
  invalid_vertical_speed <- units::set_units(10, s)
  expect_error(change_vertical_speed(aircraft_id = aircraft_id,
                                     vertical_speed = invalid_vertical_speed))

  # Give the command to change vertical speed.
  new_vertical_speed <- 10
  expect_true(change_vertical_speed(aircraft_id = aircraft_id,
                                    vertical_speed = new_vertical_speed))

  # TODO: Check that the vertical speed has changed.
})
