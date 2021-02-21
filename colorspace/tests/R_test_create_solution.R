

library("rjson")

#cat(paste(readLines("R_test_definition.json"), collapse = "\n"))
data <- fromJSON(paste(readLines("R_test_definition.json"), collapse = "\n"))
length(data)


library("colorspace")
for (i in seq_along(data)) {
    rec <- data[[i]]            # Current record
    fn  <- eval(rec$fun)        # Evaluate function
    sol <- do.call(fn, rec$arg) # Calling function with args
    data[[i]]$colors <- sol
    data[[i]]$id     <- sprintf("%06d", i)
}

# Write solution file
writeLines(toJSON(data), con = "R_test_solution.json")





