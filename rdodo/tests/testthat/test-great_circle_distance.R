require(testthat)
context("great_circle_distance function")

test_that("the great_circle_distance function works", {

  from_lat <- 51.507389
  from_lon <- 0.127806

  to_lat <- 50.6083
  to_lon <- -1.9608

  result <- great_circle_distance(from_lat, from_lon, to_lat, to_lon)

  # Compare to the result computed using the Haversine formula:
  dlat <- from_lat - to_lat
  dlon <- from_lon - to_lon

  deg2rad <- function(deg) {(deg * pi) / (180)}
  a <- (sin(deg2rad(dlat)/2))^2 + cos(deg2rad(from_lat)) * cos(deg2rad(to_lat)) * (sin(deg2rad(dlon)/2))^2
  c <- 2 * atan2(sqrt(a), sqrt(1-a))
  R <- 6378137 # Radius of the earth
  expected <- R * c

  expect_equal(result, expected = expected)

  # Check units.
  expect_true(inherits(result, "units"))
  expect_equal(units(result)[["numerator"]], expected = "m")
  expect_equal(units(result)[["denominator"]], expected = character(0))
})
