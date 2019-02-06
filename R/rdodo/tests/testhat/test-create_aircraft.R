require(testthat)
context("create_aircraft function")

test_that("the create_aircraft function works", {

  # TODO: check for Bluebird at the expected url and stop if unavailable.

  aircraft_id <- "test1234"
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

})

test_that("the create_aircraft latitude guard clause works", {

  # TODO: check for Bluebird at the expected url and stop if unavailable.

  aircraft_id <- "test1234"
  type <- "B744"
  longitude <- 0
  heading <- 0
  flight_level <- 250
  speed <- 200

  latitude <- 91
  expect_error(create_aircraft(aircraft_id = aircraft_id,
                              type = type,
                              latitude = latitude,
                              longitude = longitude,
                              heading = heading,
                              flight_level = flight_level,
                              speed = speed))

  latitude <- -90.1
  expect_error(create_aircraft(aircraft_id = aircraft_id,
                               type = type,
                               latitude = latitude,
                               longitude = longitude,
                               heading = heading,
                               flight_level = flight_level,
                               speed = speed))

  # Valid latitude:
  latitude <- -90
  expect_true(create_aircraft(aircraft_id = aircraft_id,
                               type = type,
                               latitude = latitude,
                               longitude = longitude,
                               heading = heading,
                               flight_level = flight_level,
                               speed = speed))
})

test_that("the create_aircraft longitude guard clause works", {

  # TODO: check for Bluebird at the expected url and stop if unavailable.

  aircraft_id <- "test1234"
  type <- "B744"
  latitude <- 0
  heading <- 0
  flight_level <- 250
  speed <- 200

  longitude <- 180
  expect_error(create_aircraft(aircraft_id = aircraft_id,
                               type = type,
                               latitude = latitude,
                               longitude = longitude,
                               heading = heading,
                               flight_level = flight_level,
                               speed = speed))

  longitude <- -180.1
  expect_error(create_aircraft(aircraft_id = aircraft_id,
                               type = type,
                               latitude = latitude,
                               longitude = longitude,
                               heading = heading,
                               flight_level = flight_level,
                               speed = speed))

  # Valid longitude:
  longitude <- -180
  expect_true(create_aircraft(aircraft_id = aircraft_id,
                              type = type,
                              latitude = latitude,
                              longitude = longitude,
                              heading = heading,
                              flight_level = flight_level,
                              speed = speed))
})

test_that("the create_aircraft heading guard clause works", {

  # TODO: check for Bluebird at the expected url and stop if unavailable.

  aircraft_id <- "test1234"
  type <- "B744"
  latitude <- 0
  longitude <- 0
  flight_level <- 250
  speed <- 200

  heading <- -0.1
  expect_error(create_aircraft(aircraft_id = aircraft_id,
                               type = type,
                               latitude = latitude,
                               longitude = longitude,
                               heading = heading,
                               flight_level = flight_level,
                               speed = speed))

  heading <- 360
  expect_error(create_aircraft(aircraft_id = aircraft_id,
                               type = type,
                               latitude = latitude,
                               longitude = longitude,
                               heading = heading,
                               flight_level = flight_level,
                               speed = speed))

  # Valid heading:
  heading <- 359.99
  expect_true(create_aircraft(aircraft_id = aircraft_id,
                              type = type,
                              latitude = latitude,
                              longitude = longitude,
                              heading = heading,
                              flight_level = flight_level,
                              speed = speed))
})

test_that("the create_aircraft altitude guard clause works", {

  # TODO: check for Bluebird at the expected url and stop if unavailable.

  aircraft_id <- "test1234"
  type <- "B744"
  latitude <- 0
  longitude <- 0
  heading <- 0
  speed <- 200

  altitude <- 6000
  flight_level <- 250
  expect_error(create_aircraft(aircraft_id = aircraft_id,
                               type = type,
                               latitude = latitude,
                               longitude = longitude,
                               heading = heading,
                               altitude = altitude,
                               flight_level = flight_level,
                               speed = speed))

  altitude <- 6001
  flight_level <- NULL
  expect_error(create_aircraft(aircraft_id = aircraft_id,
                               type = type,
                               latitude = latitude,
                               longitude = longitude,
                               heading = heading,
                               altitude = altitude,
                               flight_level = flight_level,
                               speed = speed))

  altitude <- -1
  flight_level <- NULL
  expect_error(create_aircraft(aircraft_id = aircraft_id,
                               type = type,
                               latitude = latitude,
                               longitude = longitude,
                               heading = heading,
                               altitude = altitude,
                               flight_level = flight_level,
                               speed = speed))

  # Valid altitude:
  altitude <- 0
  flight_level <- NULL
  expect_true(create_aircraft(aircraft_id = aircraft_id,
                              type = type,
                              latitude = latitude,
                              longitude = longitude,
                              heading = heading,
                              altitude = altitude,
                              flight_level = flight_level,
                              speed = speed))

  # Valid altitude:
  altitude <- 6000
  flight_level <- NULL
  expect_true(create_aircraft(aircraft_id = aircraft_id,
                               type = type,
                               latitude = latitude,
                               longitude = longitude,
                               heading = heading,
                               altitude = altitude,
                               flight_level = flight_level,
                               speed = speed))
})

