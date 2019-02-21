require(testthat)
context("create_aircraft function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the create_aircraft function works", {

  aircraft_id <- "test-create"
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

  aircraft_id <- "test-lat"
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

  aircraft_id <- "test-long"
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

  aircraft_id <- "test-hdg"
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

  aircraft_id <- "test-alt"
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
  aircraft_id <- "test-alt-2" # Avoid aircraft ID clash
  expect_true(create_aircraft(aircraft_id = aircraft_id,
                               type = type,
                               latitude = latitude,
                               longitude = longitude,
                               heading = heading,
                               altitude = altitude,
                               flight_level = flight_level,
                               speed = speed))
})

test_that("the create_aircraft flight_level guard clause works", {

  aircraft_id <- "test-fl"
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

  altitude <- NULL
  flight_level <- 59
  expect_error(create_aircraft(aircraft_id = aircraft_id,
                               type = type,
                               latitude = latitude,
                               longitude = longitude,
                               heading = heading,
                               altitude = altitude,
                               flight_level = flight_level,
                               speed = speed))

  # Valid flight_level:
  altitude <- NULL
  flight_level <- 60
  expect_true(create_aircraft(aircraft_id = aircraft_id,
                              type = type,
                              latitude = latitude,
                              longitude = longitude,
                              heading = heading,
                              altitude = altitude,
                              flight_level = flight_level,
                              speed = speed))
})

test_that("the create_aircraft speed guard clause works", {

  aircraft_id <- "test-spd"
  type <- "B744"
  latitude <- 0
  longitude <- 0
  heading <- 0
  flight_level <- 250

  speed <- -0.1
  expect_error(create_aircraft(aircraft_id = aircraft_id,
                               type = type,
                               latitude = latitude,
                               longitude = longitude,
                               heading = heading,
                               flight_level = flight_level,
                               speed = speed))

  # Valid speed:
  speed <- 0
  expect_true(create_aircraft(aircraft_id = aircraft_id,
                              type = type,
                              latitude = latitude,
                              longitude = longitude,
                              heading = heading,
                              flight_level = flight_level,
                              speed = speed))
})

