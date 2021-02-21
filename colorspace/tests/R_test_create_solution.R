

library("rjson")

#cat(paste(readLines("R_test_definition.json"), collapse = "\n"))
data <- fromJSON(paste(readLines("R_test_definition.json"), collapse = "\n"))
length(data)


library("colorspace")
counter <- 0
for (i in seq_along(data)) {
    rec <- data[[i]]            # Current record

    # Skip comments
    if ("_comment" %in% names(rec)) next

    # Else evaluate
    fn  <- eval(rec$fun)        # Evaluate function
    sol <- do.call(fn, rec$arg) # Calling function with args
    data[[i]]$colors <- sol
    data[[i]]$id     <- sprintf("%06d", (counter <- counter + 1))
}

# Write solution file
writeLines(toJSON(data), con = "R_test_solution.json")





