#' Get a configuration parameter
#'
#' @param param
#' The name of the config parameter.
#' @param file
#' The configuration file to read from.
#'
#' @import config utils
#' @export
config_param <- function(param, file = config_file_location()) {

  if (!file.exists(file)) {
    message(paste("Config file not found",
                  ifelse(is.null(file), yes = "", no = paste("at:", file))))

    # If a config file is not found at the default location, retrieve one
    # from the dodo repository.
    file <- config_file_location()
    if (!file.exists(file))
      file <- retrieve_config_file()

    if (!file.exists(file))
      stop("Failed to find config file.")

    message("Using config file at: ", file)
  }
  config::get(param, file = file, use_parent = FALSE)
}

# Download the config file from the dodo repository and return it's location.
retrieve_config_file <- function() {

  message("Attempting to download rdodo config file ...")
  destfile <- config_file_location()

  # Avoid overwriting an existing file.
  if (file.exists(destfile))
    stop(paste("Aborting download attempt due to conflicting file at:", destfile))

  # TODO: replace `rdodo` branch with `master` after merge.
  url <- "https://raw.githubusercontent.com/alan-turing-institute/dodo/rdodo/config.yml"
  response <- tryCatch({
    utils::download.file(url, destfile = destfile)
  },
  error=function(cond) {
    packageStartupMessage("Error downloading rdodo config file.")
  })

  if (response != 0L || !file.exists(destfile))
    stop(paste("Failed to download rdodo config file. You will need to obtain one, e.g. from:\n", url))

  # Return the path to the retrieved config file.
  destfile
}

# Returns the default config file location in the package installation directory.
config_file_location <- function() {
  file.path(system.file(package = "rdodo"), "config.yml")
}
