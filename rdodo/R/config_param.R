#' Get a configuration parameter
#'
#' @param param
#' The name of the config parameter.
#' @param file
#' The configuration file to read from.
#'
#' @import config utils
#' @export
config_param <- function(param, file = Sys.getenv("RDODO_CONFIG_FILE")) {

  # TODO:
  # If no config.yml file is found in the working directory or its immediate
  # parent, an attempt is made to download one from the rdodo repository.
  # Check that this works when importing rdodo in another package, i.e. does the
  # config package search for config.yml in the working directory or in the
  # location at which rdodo is installed?

  if (!file.exists(file))
    file <- retrieve_config_file(file)

  config::get(param, file = file, use_parent = TRUE)
}

# Download the config file from the dodo repository and return it's location.
retrieve_config_file <- function(file) {

  message("Attempting to download rdodo config file ...")

  default_filename <- "config.yml"
  destfile <- file.path(getwd(), default_filename)

  # Avoid overwriting an existing file.
  if (file.exists(destfile))
    warning(paste("rdodo config file not found at expected location:", file,
                  "\nAborting download attempt due to conflicting file at:", destfile))

  url <- "https://raw.githubusercontent.com/alan-turing-institute/dodo/master/config.yml"
  response <- tryCatch({
    utils::download.file(url, destfile = destfile)
  },
  error=function(cond) {
    packageStartupMessage("Error downloading rdodo config file.")
  })

  if (response != 0L || !file.exists(destfile))
    stop(paste("Failed to download rdodo config file. You will need to obtain one, e.g. from:\n", url))

  # Set the env variable so subsequent calls to config_param will work.
  Sys.setenv("RDODO_CONFIG_FILE" = destfile)

  # Return the path to the retrieved config file.
  destfile
}
