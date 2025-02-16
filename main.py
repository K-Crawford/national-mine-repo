import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def scrapeQuarries(longitude, latitude, radius, commodity):
    # Define the download directory
    download_dir = '/Users/katcrawford/Desktop/MINES'
    
    # Set up Chrome options to specify download directory
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    distances = [1, 5, 10, 25, 50, 100, 1000]
    distance = str(min(distances, key=lambda x: abs(x-radius)))
    print(distance)

    # Add the above options when creating the driver instance
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://mmr.osmre.gov/")

    wait = WebDriverWait(driver, 15)

    latitude_input = wait.until(EC.presence_of_element_located((By.ID, "txtLatitude")))
    driver.execute_script(f"arguments[0].value='{latitude}';", latitude_input)

    longitude_input = wait.until(EC.presence_of_element_located((By.ID, "txtLongitude")))
    driver.execute_script(f"arguments[0].value='{longitude}';", longitude_input)

    distance_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ddlDistance")))
    Select(distance_dropdown).select_by_visible_text(f"{distance} miles")

    time.sleep(2)

    commodity_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ddlCommodity")))
    select_object = Select(commodity_dropdown)

    for option in select_object.options:
        print("Commodity Option: ", option.text)

    try:
        select_object.select_by_visible_text(commodity)
        print(f"Commodity set to {commodity}")
    except Exception as e:
        print(f"Failed to set commodity: {e}")

    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        if button.text.strip().lower() == "submit":
            button.click()
            break

    time.sleep(3)

    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        if button.text.strip().lower() == "export search results":
            button.click()
            break

    # Wait for download to complete
    time.sleep(10)  # Adjust sleep time if necessary

    # Assuming the downloaded file is the only CSV in the directory
    csv_files = [f for f in os.listdir(download_dir) if f.endswith('.csv')]
    latest_file = max(csv_files, key=lambda x: os.path.getctime(os.path.join(download_dir, x)))
    latest_file_path = os.path.join(download_dir, latest_file)

    df = pd.read_csv(latest_file_path)

    print(df)

    # Save as output CSV if needed
    df.to_csv('output_table.csv', index=False)

    driver.quit()

longitude = str(-74.0060)
latitude = str(40.7128)
radius = 100
commodity = "GOLD"

scrapeQuarries(longitude, latitude, radius, commodity)