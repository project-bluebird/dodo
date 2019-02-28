# Runs whenever the package is loaded.
#
# Checks that a config.yml file exists and, if not, attempts to download one
# from the dodo repository.
#
.onLoad <- function(libname, pkgname) {

  # Check the config.yml file exists.
  config_filename <- "config.yml"

  config_file <- NA

  if (file.exists(file.path("..", config_filename)))
    config_file <- file.path("..", config_filename)
  if (file.exists(config_filename))
    config_file <- config_filename

  if (is.na(config_file))
    return(packageStartupMessage("No config.yml file found"))

  # Note: the following env variable name must match that in the config_param function.
  Sys.setenv("RDODO_CONFIG_FILE" = config_file)
  packageStartupMessage(paste("Using configuration file:", config_file))
}
