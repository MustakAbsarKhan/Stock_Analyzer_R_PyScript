import glob
import shutil
import subprocess
import platform
import time
import re
from datetime import datetime, timedelta

# Display program information and contact details
print("\n R Script Modifier")
print("\n Created by: Mohammad Mustak Absar Khan")
print(" Contact: mustak.absar.khan@gmail.com \n")

# Find the first R script file in the current directory
r_script_files = glob.glob("stock_analyzer.R")

if not r_script_files:
    print("\n No R script files found in the current directory.")
    print("\n Please place your R script file in the same folder as this program.")
    exit()

r_script_path = r_script_files[0]

# Prompt the user to enter a stock symbol
symbol = input("\n Enter a stock symbol: ")

# Prompt the user to select the start and end dates
use_default_dates = input("\n Do you want to use the default dates (1 Month)? (y/n): ")

if use_default_dates.lower() == "y":
    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")
else:
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")

# Prompt the user to select the scale for the x-axis
scale_options = ["day", "week", "month", "year"]
scale_choice = input("\n Select the scale for the x-axis (day/week/month/year): ")

if scale_choice.lower() not in scale_options:
    print("Invalid scale choice. Using the default scale (week).")
    scale_choice = "week"

# Create a backup of the original R script
backup_r_script_path = r_script_path + ".bak"
shutil.copy2(r_script_path, backup_r_script_path)

# Read the contents of the original R script
with open(r_script_path, "r") as file:
    r_script_code = file.read()

# Find the existing values of "end_date" and "start_date" in the R script
existing_end_date = re.search(r'end_date <- as.Date\("(.+?)"\)', r_script_code).group(1)
existing_start_date = re.search(r'start_date <- as.Date\("(.+?)"\)', r_script_code).group(1)

# Replace the values of the "end_date" and "start_date" variables in the R script
modified_r_script_code = r_script_code.replace('end_date <- as.Date("{}")'.format(existing_end_date),
                                               'end_date <- as.Date("{}")'.format(end_date))
modified_r_script_code = modified_r_script_code.replace('start_date <- as.Date("{}")'.format(existing_start_date),
                                                        'start_date <- as.Date("{}")'.format(start_date))

# Find the existing value of the "breaks" argument in scale_x_date() function
existing_breaks_value = re.search(r'breaks\s*=\s*"(.+?)"', modified_r_script_code).group(1)

# Replace the value of the "breaks" argument in scale_x_date() function
modified_r_script_code = modified_r_script_code.replace('breaks = "{}"'.format(existing_breaks_value),
                                                        'breaks = "{}"'.format(scale_choice))

# Write the modified R script to the original file
with open(r_script_path, "w") as file:
    file.write(modified_r_script_code)

# Detect the operating system
operating_system = platform.system()

# Determine the default RStudio executable path based on the operating system
if operating_system == "Windows":
    rstudio_path = "C:/Program Files/RStudio/bin/rstudio.exe"
elif operating_system == "Darwin":  # macOS
    rstudio_path = "/Applications/RStudio.app/Contents/MacOS/RStudio"
else:  # Linux or other systems
    rstudio_path = "/usr/bin/rstudio"

# Execute the modified R script using RStudio
subprocess.Popen([rstudio_path, r_script_path])

time.sleep(5)
while True:
    choice = input("\n Press 'q' to quit: ")
    if choice.lower() == "q":
        break