require(testthat)
context("change_speed function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the change_speed function works", {

  aircraft_id <- "test-change-speed"
  type <- "B77W"
  latitude <- 0
  longitude <- 0
  heading <- 0
  flight_level <- 300
  speed <- units::set_units(280, "knot")

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

  # Check the speed.
  position <- aircraft_position(aircraft_id)
  h_speed <- config_param("ground_speed")

  # 280 knots CAS at FL300 corresponds to 225 m/s ground speed.
  expect_equal(position[aircraft_id, h_speed], units::set_units(225, m/s))

  # Test with an invalid speed.
  invalid_speed <- -1
  expect_error(change_speed(aircraft_id = aircraft_id, speed = invalid_speed))

  expect_equal(position[aircraft_id, h_speed], units::set_units(225, m/s))

  # Test with invalid units.
  invalid_speed <- units::set_units(200, m)
  expect_error(change_speed(aircraft_id = aircraft_id, speed = invalid_speed))

  expect_equal(position[aircraft_id, h_speed], units::set_units(225, m/s))

  # Give the command to change speed.
  new_speed <- units::set_units(400, "knot")
  expect_true(change_speed(aircraft_id = aircraft_id, speed = new_speed))

  # Wait for the speed to increase.
  expect_true(wait(aircraft_id, property = h_speed, operator = `>`,
                   initial_value = units::set_units(226, m/s)))

  # Check that the speed has changed.
  new_position <- aircraft_position(aircraft_id)
  expect_true(new_position[aircraft_id, h_speed] > units::set_units(226, m/s))
})
