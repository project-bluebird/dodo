#' Get a configuration parameter
#'
#' @param param
#' The name of the config parameter.
#' @param file
#' The configuration file to read from.
#'
#' @return The value of the requested configuration parameter. An error is
#' thrown if the given parameter name is not found in the config file.
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

    message("Using rdodo config file at: ", file)
  }
  ret <- config::get(param, file = file, use_parent = FALSE)

  # Throw an error if the given config parameter is not found.
  if (is.null(ret))
    stop(paste("Config parameter", param, "not found"))

  ret
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
  message("Downloaded config file to: ", destfile)
  destfile
}

# Returns the default config file location. Normally this is the package
# installation directory, except when running tests with cmd+T or running
# R CMD CHECK, in which case it is the parent of the package source root.
config_file_location <- function() {

  config_filename <- "config.yml"

  # Note that when running tests with cmd+T or running R CMD CHECK this function
  # returns the package source root directory, *not* the installation directory.
  path <- system.file(package = "rdodo")

  if (file.exists(file.path(path, config_filename)))
    return(file.path(path, config_filename))

  # If running tests/R CMD CHECK, the config file will not be in the expected
  # location. In that case, modify the path so it points to the parent "dodo" of
  # the rdodo source package directory (which contains the development config file).
  split_path <- strsplit(path, split = .Platform$file.sep)
  source_parent <- "dodo"
  if (source_parent %in% split_path[[1]]) {
    n <- which(split_path[[1]] == source_parent)
    path <- paste(head(split_path[[1]], n = n), collapse = .Platform$file.sep)
  }

  file.path(path, config_filename)
}
