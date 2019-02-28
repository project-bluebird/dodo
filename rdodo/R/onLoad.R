# Runs whenever the package is loaded.
#
# Checks that a config.yml file exists and, if not, attempts to download one
# from the dodo repository.
#
.onLoad <- function(libname, pkgname) {

  # TODO:
  # If no config.yml file is found in the working directory or its immediate
  # parent, an attempt is made to download one from the rdodo repository.
  # Check that this works when importing rdodo in another package, i.e. does the
  # config package search for config.yml in the working directory or in the
  # location at which rdodo is installed?

  # Check the config.yml file exists.
  config_filename <- "config.yml"

  config_file <- NA

  if (file.exists(file.path("..", config_filename)))
    config_file <- file.path("..", config_filename)
  if (file.exists(config_filename))
    config_file <- config_filename

  # If necessary, pick up the config file from the dodo repository. Note there
  # is no danger of overwriting an existing file, given the above.
  if (is.na(config_file)) {
    packageStartupMessage("No config.yml file found. Attempting to download one...")

    url <- "https://raw.githubusercontent.com/alan-turing-institute/dodo/master/config.yml"
    response <- tryCatch({
      utils::download.file(url, destfile = file.path(getwd(), config_filename))
    },
    error=function(cond) {
      packageStartupMessage("Error downloading rdodo config.yml file.")
      stop(paste(conditionMessage(cond)))
    })

    if (response != 0L || !file.exists(config_filename))
      warning(paste("Failed to download rdodo config.yml file. You will need to obtain one, e.g. from:\n", url))
    packageStartupMessage(paste("Downloaded rdodo configuration file:", config_filename))

    config_file <- config_filename
  }
  packageStartupMessage(paste("Using configuration file:", config_file))
}
