require(testthat)
context("geodesic_distance function")

test_that("the geodesic_distance function works", {

  from_lat <- 51.507389
  from_lon <- 0.127806

  to_lat <- 50.6083
  to_lon <- -1.9608

  result <- geodesic_distance(from_lat, from_lon, to_lat, to_lon)

  # Compare to the result calculated using ArcGIS (to within 1% error):
  expect_equal(result, expected = 1000*176.92, tolerance = 0.01)
})
