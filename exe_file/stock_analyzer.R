# List of libraries to check
libraries <- c("quantmod", "ggplot2", "tidyr", "lubridate")

# Check if each library is installed
for (lib in libraries) {
  if (!require(lib, character.only = TRUE)) {
    cat("\n", lib, "library is about to get installed!\n")
    
    # If the library is not installed, install it
    install.packages(lib)
    # Load the library after installation
    library(lib, character.only = TRUE)
  }
  else{
    cat("\n", lib, "library is already installed!\n")
  }
}


library(quantmod)
library(ggplot2)
library(tidyr)
library(lubridate)

symbol <- "AAPL" # input your desired stock symbol (working in yahoo finance)

end_date <- as.Date("2023-05-24")
start_date <- as.Date("2023-04-24")

# Fetch stock data
stock_data <- getSymbols(Symbols = symbol, src = "yahoo", from = start_date, to = end_date, auto.assign = FALSE)

# Extract required prices
opening_prices <- stock_data[, paste(symbol, "Open", sep = ".")]
closing_prices <- stock_data[, paste(symbol, "Close", sep = ".")]
adjusted_prices <- stock_data[, paste(symbol, "Adjusted", sep = ".")]
high_prices <- stock_data[, paste(symbol, "High", sep = ".")]
low_prices <- stock_data[, paste(symbol, "Low", sep = ".")]

# Create a data frame with the prices
stock_data_df <- data.frame(
  Date = index(stock_data),
  opening_prices,
  closing_prices,
  adjusted_prices,
  high_prices,
  low_prices
)

print(stock_data_df)

# Filter data within the desired date range
filtered_data <- stock_data_df[stock_data_df$Date >= start_date & stock_data_df$Date <= end_date, ]

# Convert the filtered data frame to long format
stock_data_long <- tidyr::gather(filtered_data, key = "Price_Type", value = "Price", -Date)

# Calculate x-axis limits
x_limits <- range(filtered_data$Date)

# Plot using ggplot2
ggplot(stock_data_long, aes(x = Date, y = Price, color = Price_Type)) +
  geom_line(aes(alpha = Price_Type), size = 1) +
  labs(title = expression(bold(paste("Stock Prices for ", symbol)))) +
  scale_color_manual(
    values = c("blue", "red", "green", "orange", "purple"),
    labels = c("Opening Prices", "Closing Prices", "Adjusted Prices", "High Prices", "Low Prices")
  ) +
  scale_alpha_manual(
    values = c("Opening Prices" = 1, "Closing Prices" = 1, "Adjusted Prices" = 0.7, "High Prices" = 0.7, "Low Prices" = 0.7)
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(size = 16, face = "bold", margin = margin(b = 20)),
    axis.title = element_text(size = 12, face = "bold"),
    axis.text = element_text(size = 10),
    legend.position = "bottom",
    legend.title = element_blank(),
    panel.grid.major = element_line(color = "gray80"),
    panel.grid.minor = element_blank(),
    panel.border = element_rect(color = "black", fill = NA, size = 1),
    plot.margin = margin(20, 30, 20, 20)
  ) +
  scale_x_date(
    limits = x_limits,
    date_labels = "%Y-%m-%d",
    breaks = "week"
    #'hour', 'day', 'week', 'month' or 'year'
  )

