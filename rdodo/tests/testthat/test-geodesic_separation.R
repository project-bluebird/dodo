require(testthat)
context("geodesic_separation function")

skip_if_not(found_bluebird(), message = "BlueBird not found: tests skipped.")

# Reset the simulation to ensure no aircraft exist initially.
reset_simulation()

test_that("the geodesic_separation function works", {

  from_aircraft_id <- toupper("test-geodesic-sep-from")
  type <- "B744"
  latitude <- 51.507389
  longitude <- 0.127806
  heading <- 0
  flight_level <- 250
  speed <- 200

  expect_true(create_aircraft(aircraft_id = from_aircraft_id,
                              type = type,
                              latitude = latitude,
                              longitude = longitude,
                              heading = heading,
                              flight_level = flight_level,
                              speed = speed))

  to_aircraft_id <- toupper("test-geodesic-sep-to")
  type <- "B747"
  latitude <- 50.6083
  longitude <- -1.9608
  heading <- 0
  flight_level <- 250
  speed <- 200

  expect_true(create_aircraft(aircraft_id = to_aircraft_id,
                              type = type,
                              latitude = latitude,
                              longitude = longitude,
                              heading = heading,
                              flight_level = flight_level,
                              speed = speed))


  result <- geodesic_separation(from_aircraft_id, to_aircraft_id)

  # Check the return type:
  expect_true(is.data.frame(result))
  expect_identical(from_aircraft_id, rownames(result))
  expect_identical(to_aircraft_id, colnames(result))

  # Check the units:
  sapply(colnames(result), FUN = function(colname) {
    expect_true(inherits(result[[colname]], "units"))
    expect_equal(units(result[[colname]])[["numerator"]], expected = "m")
    expect_equal(units(result[[colname]])[["denominator"]], expected = character(0))
  })

  # Compare to the result calculated using ArcGIS (to within 1% error):
  expect_equal(result[from_aircraft_id, to_aircraft_id],
               expected = 1000*176.92, tolerance = 0.01)
})

test_that("the geodesic_separation function works with vector arguments", {

  aircraft_id_1 <- toupper("test-geodesic-sep-1")
  type <- "B744"
  latitude <- 51.507389
  longitude <- 0.127806
  heading <- 0
  flight_level <- 250
  speed <- 200

  expect_true(create_aircraft(aircraft_id = aircraft_id_1,
                              type = type,
                              latitude = latitude,
                              longitude = longitude,
                              heading = heading,
                              flight_level = flight_level,
                              speed = speed))

  aircraft_id_2 <- toupper("test-geodesic-sep-2")
  type <- "B747"
  latitude <- 50.6083
  longitude <- -1.9608
  heading <- 0
  flight_level <- 250
  speed <- 200

  expect_true(create_aircraft(aircraft_id = aircraft_id_2,
                              type = type,
                              latitude = latitude,
                              longitude = longitude,
                              heading = heading,
                              flight_level = flight_level,
                              speed = speed))


  # Test with both from & to vector arguments.
  from_aircraft_id <- c(aircraft_id_1, aircraft_id_2)
  to_aircraft_id <- c(aircraft_id_1, aircraft_id_2)

  result <- geodesic_separation(from_aircraft_id = from_aircraft_id,
                                to_aircraft_id = to_aircraft_id)

  # Check the return type:
  expect_true(is.data.frame(result))
  expect_identical(from_aircraft_id, rownames(result))
  expect_identical(to_aircraft_id, colnames(result))

  # Check the units:
  sapply(colnames(result), FUN = function(colname) {
    expect_true(inherits(result[[colname]], "units"))
    expect_equal(units(result[[colname]])[["numerator"]], expected = "m")
    expect_equal(units(result[[colname]])[["denominator"]], expected = character(0))
  })

  # Compare to the result calculated using ArcGIS (to within 1% error):
  expect_equal(result[aircraft_id_1, aircraft_id_2],
               expected = 1000*176.92, tolerance = 0.01)
  expect_equal(result[aircraft_id_2, aircraft_id_1],
               expected = 1000*176.92, tolerance = 0.01)

  expect_equal(result[aircraft_id_1, aircraft_id_1], expected = 0)
  expect_equal(result[aircraft_id_2, aircraft_id_2], expected = 0)

  # Now test with only the "to" vector argument.
  from_aircraft_id <- aircraft_id_1
  to_aircraft_id <- c(aircraft_id_1, aircraft_id_2)

  result <- geodesic_separation(from_aircraft_id = from_aircraft_id,
                                to_aircraft_id = to_aircraft_id)

  # Check the return type:
  expect_true(is.data.frame(result))
  expect_identical(from_aircraft_id, rownames(result))
  expect_identical(to_aircraft_id, colnames(result))

  # Check the units:
  sapply(colnames(result), FUN = function(colname) {
    expect_true(inherits(result[[colname]], "units"))
    expect_equal(units(result[[colname]])[["numerator"]], expected = "m")
    expect_equal(units(result[[colname]])[["denominator"]], expected = character(0))
  })

  # Compare to the result calculated using ArcGIS (to within 1% error):
  expect_equal(result[aircraft_id_1, aircraft_id_1], expected = 0)
  expect_equal(result[aircraft_id_1, aircraft_id_2],
               expected = 1000*176.92, tolerance = 0.01)

  # Now test with only the "from" vector argument.
  from_aircraft_id <- c(aircraft_id_1, aircraft_id_2)
  to_aircraft_id <- aircraft_id_2

  result <- geodesic_separation(from_aircraft_id = from_aircraft_id,
                                to_aircraft_id = to_aircraft_id)

  # Check the return type:
  expect_true(is.data.frame(result))
  expect_identical(from_aircraft_id, rownames(result))
  expect_identical(to_aircraft_id, colnames(result))

  # Check the units:
  sapply(colnames(result), FUN = function(colname) {
    expect_true(inherits(result[[colname]], "units"))
    expect_equal(units(result[[colname]])[["numerator"]], expected = "m")
    expect_equal(units(result[[colname]])[["denominator"]], expected = character(0))
  })

  # Compare to the result calculated using ArcGIS (to within 1% error):
  expect_equal(result[aircraft_id_1, aircraft_id_2],
               expected = 1000*176.92, tolerance = 0.01)
  expect_equal(result[aircraft_id_2, aircraft_id_2], expected = 0)
})

