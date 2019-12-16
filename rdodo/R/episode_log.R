#' Download the episode log file
#'
#' Downloads the episode log and saves it to file in the given \code{path}, or
#' the working directory by default, under a subdirectory named \code{logs}.
#'
#' @param path
#' (Optional) The directory path under which the log file will be saved.
#'
#' @return
#' The relative path to the saved episode log file, if successful. Otherwise an
#' error is thrown.
#'
#' @examples
#' \dontrun{
#' episode_log()
#' }
#'
#' @import httr
#' @export
episode_log <- function(path = "") {

  # Construct the API call URL.
  endpoint <- config_param("endpoint_episode_log")
  url <- construct_endpoint_url(endpoint)

  response <- tryCatch({
    httr::GET(url)
  },
  error=function(cond) {
    stop(paste(conditionMessage(cond)))
  })

  validate_response(response)

  # Parse the response & extract the target log file path & filename.
  parsed <- jsonlite::fromJSON(httr::content(response, "text"),
                               simplifyVector = FALSE)

  logs_dir <- "logs"
  path_prefix <- paste0(logs_dir, .Platform$file.sep)
  rel_file <- strsplit(x = parsed[["cur_ep_file"]], split = path_prefix)[[1]][2]
  filename <- tail(strsplit(x = rel_file, split = .Platform$file.sep)[[1]], n = 1)
  subs <- head(strsplit(x = rel_file, split = .Platform$file.sep)[[1]], n = -1)

  rel_path <- file.path(logs_dir, subs)
  if (nchar(path) > 0)
    rel_path <- file.path(path, rel_path)

  if (!dir.exists(rel_path))
    dir.create(rel_path, recursive = TRUE)

  # Construct the full path to the log file.
  full_path <- file.path(rel_path, filename)

  # Write the log file.
  conn <- file(full_path)
  writeLines(unlist(parsed[["lines"]]), con = conn)
  close(conn)

  full_path
}
