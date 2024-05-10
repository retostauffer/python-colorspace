# Series of colors which are converted into different color spaces
# to check the python colorspace colorlib (transformations between
# different color spaces).
#
# Output will be stored as a json file, used by pytest.


library("rjson")
library("colorspace")

# Starting to set up output file
result <- list(meta = list(), colors = list())
result$meta$created <- format(Sys.Date(), "%Y-%m-%d")
result$meta$version <- as.character(packageVersion("colorspace"))

# Using 10 colors from the infamous color space + its darker
# and lighter friends. These are the `hexcols`.
hexcols <- rainbow(10)
hexcols <- c(hexcols, darken(hexcols, 0.5), lighten(hexcols, 0.5))
result$colors$hexcols <- hexcols

# Helper function to extract the coordinates to get the
# structure we need for the JSON file.
get_data <- function(x) {
    as.list(as.data.frame(x@coords))
}

# -------------------------------------------------------
# Convert into different color spaces
# -------------------------------------------------------
cols_sRGB          <- hex2RGB(hexcols)
result$colors$sRGB <- get_data(cols_sRGB)

cols_RGB           <- as(cols_sRGB, "RGB")
result$colors$RGB  <- get_data(cols_RGB)

cols_HLS          <- as(cols_sRGB, "HLS")
result$colors$HLS <- get_data(cols_HLS)

cols_HSV          <- as(cols_sRGB, "HSV")
result$colors$HSV <- get_data(cols_HSV)

cols_XYZ             <- as(cols_sRGB, "XYZ")
result$colors$CIEXYZ <- get_data(cols_XYZ)

cols_LAB             <- as(cols_sRGB, "LAB")
result$colors$CIELAB <- get_data(cols_LAB)

cols_LUV             <- as(cols_sRGB, "LUV")
result$colors$CIELUV <- get_data(cols_LUV)

cols_polarLAB          <- as(cols_sRGB, "polarLAB")
result$colors$polarLAB <- get_data(cols_polarLAB)

cols_polarLUV          <- as(cols_sRGB, "polarLUV")
result$colors$polarLUV <- get_data(cols_polarLUV)

# Saving result
jsonfile <- "R_test_colorlib_solution.json"
cat("Writing file:", jsonfile, "\n")
writeLines(toJSON(result), con = jsonfile)



