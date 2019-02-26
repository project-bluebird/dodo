require(testthat)
context("aircraft_position function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the aircraft_position function works with invalid aircraft ID", {

  aircraft_id <- "NO-SUCH-AIRCRAFT"
  expect_error(aircraft_position(aircraft_id), regexp = "Invalid")
})

test_that("the aircraft_position function works with scalar argument", {

  aircraft_id <- "test-aircraft-position"
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

  # Get its position.
  result <- aircraft_position(aircraft_id)

  expect_true(is.data.frame(result))
  expect_identical(object = nrow(result), expected = 1L)
  expect_identical(object = rownames(result), expected = aircraft_id)
  expected <- c("altitude", "ground_speed", "latitude", "longitude", "vertical_speed")
  expect_identical(object = colnames(result), expected = expected)

  expect_identical(object = result[aircraft_id, "altitude"],
                   expected = flight_level * 100)

  # Ground speed differs from indicated speed, so allow a tolerance of +/- 5%.
  expect_equal(object = result[aircraft_id, "ground_speed"],
                   expected = speed, tolerance = 0.05)

  expect_true(object = result[aircraft_id, "latitude"] > 0)
  expect_identical(object = result[aircraft_id, "longitude"], expected = 0)
  expect_identical(object = result[aircraft_id, "vertical_speed"], expected = 0)
})

test_that("the aircraft_position function works with vector argument", {

  # Create two aircraft.
  aircraft_id_1 <- "test-aircraft-position-1"
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

  aircraft_id_2 <- "test-aircraft-position-2"
  type_2 <- "C744"
  latitude_2 <- 0
  longitude_2 <- 0
  heading_2 <- 180
  flight_level_2 <- 450
  speed_2 <- 400

  expect_true(create_aircraft(aircraft_id = aircraft_id_2,
                              type = type_2,
                              latitude = latitude_2,
                              longitude = longitude_2,
                              heading = heading_2,
                              flight_level = flight_level_2,
                              speed = speed_2))

  # Get their positions.
  result <- aircraft_position(c(aircraft_id_1, aircraft_id_2))

  expect_true(is.data.frame(result))
  expect_identical(object = nrow(result), expected = 2L)
  expect_identical(object = rownames(result),
                   expected = c(aircraft_id_1, aircraft_id_2))
  expected <- c("altitude", "ground_speed", "latitude", "longitude",
                "vertical_speed")
  expect_identical(object = colnames(result), expected = expected)

  expect_identical(object = result[aircraft_id_1, "altitude"],
                   expected = flight_level_1 * 100)

  # Ground speed differs from indicated speed, so allow a tolerance of +/- 5%.
  expect_equal(object = result[aircraft_id_1, "ground_speed"],
               expected = speed_1, tolerance = 0.05)

  expect_true(object = result[aircraft_id_1, "latitude"] > 0)
  expect_identical(object = result[aircraft_id_1, "longitude"], expected = 0)
  expect_identical(object = result[aircraft_id_1, "vertical_speed"], expected = 0)

  expect_identical(object = result[aircraft_id_2, "altitude"],
                   expected = flight_level_2 * 100)

  # Ground speed differs from indicated speed, so allow a tolerance of +/- 5%.
  expect_equal(object = result[aircraft_id_2, "ground_speed"],
               expected = speed_2, tolerance = 0.05)

  expect_true(object = result[aircraft_id_2, "latitude"] < 0)
  expect_identical(object = result[aircraft_id_2, "longitude"], expected = 0)
  expect_identical(object = result[aircraft_id_2, "vertical_speed"], expected = 0)
})
