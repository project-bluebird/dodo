#' Check communication with BlueBird
#'
#' @return A boolean, \code{TRUE} indicates a valid response was received from
#' the BlueBird API.
#'
#' @examples
#' \dontrun{
#' found_bluebird()
#' }
#'
#' @export
found_bluebird <- function() {

  response <- tryCatch({
      # TODO (temporary use of the "ic" command to check communication):
      httr::POST(url = construct_endpoint_url(endpoint = "ic"))
    },
    error=function(cond) {
      message(paste(cond))
      return(FALSE)
    }
  )

  if (identical(response, FALSE))
    return(FALSE)

  # TODO: Temporary:
  if (httr::status_code(response) == 418)
    return(TRUE)

  # 202 status code: Accepted for processing.
  if (httr::status_code(response) == 202)
    return(TRUE)

  FALSE
}
