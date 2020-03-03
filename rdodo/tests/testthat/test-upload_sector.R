require(testthat)
context("upload_sector function")

test_that("the upload_sector function works", {

  filename <- system.file("dodo-test-sector.geojson", package="rdodo")
  sector_name <- "test-sector"
  result <- upload_sector(filename, sector_name = "test-sector")

  expect_equal(result, expected = TRUE)
})
