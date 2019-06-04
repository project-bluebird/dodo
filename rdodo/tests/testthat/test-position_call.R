require(testthat)
context("position_call function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the position_call function works when there are no aircraft", {

  # Expect an empty list when there are no aircraft in the simulation and no
  # aircraft_id is passed.
  expect_identical(position_call(), expected = list())
})

test_that("the position_call function works with an invalid aircraft ID", {

  # Missing aircraft_id (i.e. not found in the simulation).
  invalid_id <- "NoSuchAircraft"

  # Expect a list containing an empty list.
  expected <- list(list()); names(expected) <- invalid_id
  expect_identical(position_call(invalid_id), expected = expected)
})

test_that("the position_call function works with a valid aircraft ID", {

  aircraft_id <- "testPositionCall"
  type <- "B744"
  latitude <- 0
  longitude <- 0
  heading <- 0
  flight_level <- 250
  speed <- 200

  # Create an aircraft.
  expect_true(create_aircraft(aircraft_id = aircraft_id,
                              type = type,
                              latitude = latitude,
                              longitude = longitude,
                              heading = heading,
                              flight_level = flight_level,
                              speed = speed))

  # aircraft_ids are uppercase.
  aircraft_id <- toupper(aircraft_id)

  # Get its position.
  result <- position_call(aircraft_id)

  expect_true(is.list(result))
  expect_identical(names(result), c(aircraft_id, config_param("simulator_time")))

  expected <- c("actype", "alt", "gs", "lat", "lon", "vs")
  expect_true(all(expected %in% names(result[[aircraft_id]])))

  expect_true(object = result[[aircraft_id]][["lat"]] > 0)
  expect_equal(object = result[[aircraft_id]][["lon"]], expected = 0)
  expect_equal(object = result[[aircraft_id]][["vs"]], expected = 0)

  # Check for the sim_t datum.
  expect_true(is.integer(result[[config_param("simulator_time")]]))
  expect_true(result[[config_param("simulator_time")]] >= 0)
})

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the position_call function works with no argument", {

  # Create an aircraft.
  aircraft_id_1 <- "testPositionCall1"
  type_1 <- "B744"
  latitude_1 <- 0
  longitude_1 <- 0
  heading_1 <- 0
  flight_level_1 <- 250
  speed_1 <- 200

  expect_true(create_aircraft(aircraft_id = aircraft_id_1,
                              type = type_1,
                              latitude = latitude_1,
                              longitude = longitude_1,
                              heading = heading_1,
                              flight_level = flight_level_1,
                              speed = speed_1))

  # Get all aircraft positions.
  result <- position_call()

  # In the returned list aircraft_ids are uppercase.
  aircraft_id_1 <- toupper(aircraft_id_1)

  expect_true(is.list(result))
  expect_identical(names(result), c(aircraft_id_1, config_param("simulator_time")))

  expected <- c("actype", "alt", "gs", "lat", "lon", "vs")
  expect_true(all(expected %in% names(result[[aircraft_id_1]])))

  expect_true(object = result[[aircraft_id_1]][["lat"]] > 0)
  expect_equal(object = result[[aircraft_id_1]][["lon"]], expected = 0)
  expect_equal(object = result[[aircraft_id_1]][["vs"]], expected = 0)

  # Check for the sim_t datum.
  expect_true(is.integer(result[[config_param("simulator_time")]]))
  expect_true(result[[config_param("simulator_time")]] >= 0)

  # Create a second aircraft.
  aircraft_id_2 <- "testPositionCall2"
  type_2 <- "C744"
  latitude_2 <- 0
  longitude_2 <- 0
  heading_2 <- 180
  flight_level_2 <- 300
  speed_2 <- 220

  expect_true(create_aircraft(aircraft_id = aircraft_id_2,
                              type = type_2,
                              latitude = latitude_2,
                              longitude = longitude_2,
                              heading = heading_2,
                              flight_level = flight_level_2,
                              speed = speed_2))

  # Get all aircraft positions.
  result <- position_call()

  # In the returned list aircraft_ids are uppercase.
  aircraft_id_2 <- toupper(aircraft_id_2)

  expect_true(is.list(result))
  expect_identical(names(result), c(aircraft_id_1, aircraft_id_2,
                                    config_param("simulator_time")))

  expected <- c("alt", "gs", "lat", "lon", "vs")
  expect_true(all(expected %in% names(result[[aircraft_id_1]])))
  expect_true(all(expected %in% names(result[[aircraft_id_2]])))

  expect_true(object = result[[aircraft_id_1]][["lat"]] > 0)
  expect_equal(object = result[[aircraft_id_1]][["lon"]], expected = 0)
  expect_equal(object = result[[aircraft_id_1]][["vs"]], expected = 0)

  expect_true(object = result[[aircraft_id_2]][["lat"]] < 0)
  expect_equal(object = result[[aircraft_id_2]][["lon"]], expected = 0)
  expect_equal(object = result[[aircraft_id_2]][["vs"]], expected = 0)

  # Check for the sim_t datum.
  expect_true(is.integer(result[[config_param("simulator_time")]]))
  expect_true(result[[config_param("simulator_time")]] >= 0)
})
