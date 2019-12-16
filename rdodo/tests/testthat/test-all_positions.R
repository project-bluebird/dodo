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
  expected <- c(config_param("aircraft_type"),
                config_param("altitude"),
                config_param("ground_speed"),
                config_param("latitude"),
                config_param("longitude"),
                config_param("vertical_speed"))
  expect_identical(object = colnames(result), expected = expected)
})

test_that("the all_positions function works when aircraft exist", {

  # Create an aircraft.
  aircraft_id_1 <- "testAircraftPosition1"
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

  # Get all positions.
  result <- all_positions()

  # Aircraft IDs are converted to uppercase.
  aircraft_id_1 <- toupper(aircraft_id_1)

  expect_true(is.data.frame(result))
  expect_identical(object = nrow(result), expected = 1L)
  expect_identical(object = rownames(result), expected = aircraft_id_1)
  expected <- c(config_param("aircraft_type"),
                config_param("altitude"),
                config_param("ground_speed"),
                config_param("latitude"),
                config_param("longitude"),
                config_param("vertical_speed"))
  expect_identical(object = colnames(result), expected = expected)

  expect_equal(object = result[aircraft_id_1, "altitude"],
               expected = flight_level_1 * 100)

  # Aircaft initial speed may differ from specified speed.
  expect_true(result[aircraft_id_1, "ground_speed"] > set_units(150, m/s))

  expect_true(object = result[aircraft_id_1, "latitude"] > 0)
  expect_equal(object = result[aircraft_id_1, "longitude"], expected = 0)
  expect_equal(object = result[aircraft_id_1, "vertical_speed"], expected = 0)

  # Create another aircraft.
  aircraft_id_2 <- "testAircraftPosition2"
  type_2 <- "C744"
  latitude_2 <- 0
  longitude_2 <- 0
  heading_2 <- 180
  flight_level_2 <- 200
  speed_2 <- 300

  expect_true(create_aircraft(aircraft_id = aircraft_id_2,
                              type = type_2,
                              latitude = latitude_2,
                              longitude = longitude_2,
                              heading = heading_2,
                              flight_level = flight_level_2,
                              speed = speed_2))

  # Get all positions.
  result <- all_positions()

  # Aircraft IDs are converted to uppercase.
  aircraft_id_2 <- toupper(aircraft_id_2)

  expect_true(is.data.frame(result))
  expect_identical(object = nrow(result), expected = 2L)
  expect_identical(object = rownames(result),
                   expected = c(aircraft_id_1, aircraft_id_2))
  expected <- c(config_param("aircraft_type"),
                config_param("altitude"),
                config_param("ground_speed"),
                config_param("latitude"),
                config_param("longitude"),
                config_param("vertical_speed"))
  expect_identical(object = colnames(result), expected = expected)

  expect_equal(object = result[aircraft_id_1, "altitude"],
                   expected = flight_level_1 * 100)

  # Aircaft initial speed may differ from specified speed.
  expect_true(result[aircraft_id_1, "ground_speed"] > set_units(150, m/s))

  expect_true(object = result[aircraft_id_1, "latitude"] > 0)
  expect_equal(object = result[aircraft_id_1, "longitude"], expected = 0)
  expect_equal(object = result[aircraft_id_1, "vertical_speed"], expected = 0)

  expect_equal(object = result[aircraft_id_2, "altitude"],
                   expected = flight_level_2 * 100)

  # Aircaft initial speed may differ from specified speed.
  expect_true(result[aircraft_id_2, "ground_speed"] > set_units(150, m/s))

  expect_true(object = result[aircraft_id_2, "latitude"] < 0)
  expect_equal(object = result[aircraft_id_2, "longitude"], expected = 0)
  expect_equal(object = result[aircraft_id_2, "vertical_speed"], expected = 0)
})
