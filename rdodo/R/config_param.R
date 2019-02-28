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

# Returns the default config file location. Normally this is the package
# installation directory, except when running tests with cmd+T or running
# R CMD CHECK, in which case it is the parent of the package source root.
config_file_location <- function() {

  config_filename <- "config.yml"

  # Note that when running tests with cmd+T or running R CMD CHECK this function
  # returns the package source subdirectory rdodo/inst/, *not* the installation
  # directory.
  path <- system.file(package = "rdodo")

  # If running tests/R CMD CHECK, strip rdodo/inst from the end of the path so
  # it points to the parent of the rdodo package root directory.
  split_path <- strsplit(path, split = .Platform$file.sep)
  if (identical(tail(split_path[[1]], n = 1), "inst"))
    path <- paste(head(split_path[[1]], n = length(split_path[[1]]) - 2),
                       collapse = .Platform$file.sep)

  file.path(path, config_filename)
}
