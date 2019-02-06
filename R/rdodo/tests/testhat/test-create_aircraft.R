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
