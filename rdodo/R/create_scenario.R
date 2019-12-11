#' Create a scenario
#'
#' Upload a scenario file from the local machine to the running simulator.
#'
#' @param filename
#' The path to a scenario file on the local machine.
#' @param scenario
#' The name to store scenario under on the simulator host.
#' @return
#' \code{TRUE} if successful. Otherwise \code{FALSE} and an error is thrown.
#'
#' @examples
#' \dontrun{
#' create_scenario(system.file("dodo-test-scenario.scn", package = "rdodo"),
#' scenario = "dodo-test-scenario")
#' }
#'
#' @export
create_scenario <- function(filename, scenario) {

  stopifnot(is.character(filename), length(filename) == 1)
  stopifnot(is.character(scenario), length(scenario) == 1)

  # TODO: replace string literals with config parameters from Bluebird.
  body <- list("scn_name" = scenario)

  # Read lines from the file & add to the "content" element of the request body.
  conn <- file(filename, open="r")
  body <- c(body, list("content" = readLines(conn)))
  close(conn)
  post_call(endpoint = config_param("endpoint_create_scenario"), body = body)
}
