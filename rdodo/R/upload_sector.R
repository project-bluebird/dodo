#' Upload a sector
#'
#' @param filename
#' The path to a sector GeoJSON file on the local machine.
#' @param sector_name
#' The name to store the sector under.
#'
#' @return A boolean, \code{TRUE} indicates that the sector was uploaded
#' successfully.
#'
#' @examples
#' \dontrun{
#' filename <- system.file("dodo-test-sector.geojson", package="rdodo")
#' sector_name <- "test-sector"
#' upload_sector(filename, sector_name = "test-sector")
#' }
#'
#' @export
upload_sector <- function(filename, sector_name) {

  stopifnot(file.exists(filename))
  stopifnot(length(sector_name) == 1 && nchar(sector_name) > 0)

  content <- jsonlite::read_json(filename)
  body <- list("name" = sector_name, "content" = content)

  post_call(endpoint = config_param("endpoint_upload_sector"), body = body)
}
