from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

import pandas as pd


driver = webdriver.Chrome()

# Open Dice.com
driver.get('https://www.dice.com/home/home-feed')

email_field = driver.find_element(By.XPATH, '//*[@id="email"]')
password_field = driver.find_element(By.XPATH, '//*[@id="password"]')
login_button = driver.find_element(By.XPATH, '//*[@id="loginDataSubmit"]/div[3]/div/button')

# Enter the login credentials
email_field.send_keys('shaiknadeem0591@gmail.com')
password_field.send_keys('Neeha@123')

# Click the login button
login_button.click()

# Wait for a few seconds to ensure the login process completes (you can adjust the wait time as needed)
time.sleep(5)

# Create an empty list to store job details
job_details = []

# Initialize the page number
page_number = 1

while True:
    # Define the base URL for job listings with the page number inserted
    base_url = f'https://www.dice.com/jobs?radius=30&radiusUnit=mi&page={page_number}&pageSize=20&language=en'
    
    # Navigate to the current page
    driver.get(base_url)

    # Wait for a reasonable amount of time for the page to load
    time.sleep(10)  # You can adjust the wait time as needed

    # Get the page source and parse it with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all the job listings
    job_listings = soup.find_all('div', class_='card search-card')

    # Check if there are job listings on the current page
    if not job_listings:
        print(f"No job listings found on page {page_number}. Stopping the scraping process.")
        break

    # Iterate through the job listings and extract details
    for job_listing in job_listings:
        job_title = job_listing.find('a', class_='card-title-link bold').text.strip()
        company_name = job_listing.find('a', class_='ng-star-inserted').text.strip()
        location_element = job_listing.find('span', class_='search-result-location')
        location = location_element.text.strip() if location_element else 'Not Mentioned'
        description = job_listing.find('div', class_='card-description').text.strip()
        posted_date_element = job_listing.find('span', class_='posted-date')
        posted_date = posted_date_element.text.strip() if posted_date_element else 'Not Mentioned'

        # Append the job details to the list
        job_details.append([job_title, company_name, location, description, posted_date])

    # Increment the page number for the next iteration
    page_number += 1

# Create a DataFrame from the list of job details
df = pd.DataFrame(job_details, columns=['Job Title', 'Company Name', 'Location', 'Description', 'Posted Date'])

# Print the DataFrame
print(df)

# Save the DataFrame to an Excel file
df.to_excel('job_listings.xlsx', index=False)

# Close the browser when done.
driver.quit()