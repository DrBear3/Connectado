import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


def scrape_apprenticeship_site(keyword):
    url = "https://www.apprenticeship.gov/apprenticeship-job-finder"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)

    jobs = []

    job_selector = ".pop-listing-card"
    title_selector = ".card-title"
    org_selector = ".card-organization"
    location_selector = ".location-div"

    job_elements = driver.find_elements(By.CSS_SELECTOR, job_selector)
    print(f"Found {len(job_elements)} job elements.")

    for job in job_elements:
        try:
            title = job.find_element(By.CSS_SELECTOR, title_selector).text
            organization = job.find_element(By.CSS_SELECTOR, org_selector).text
            location = job.find_element(By.CSS_SELECTOR, location_selector).text

            # Filter based on keyword
            if keyword.lower() in title.lower() or keyword.lower() in organization.lower():
                jobs.append({
                    "Title": title.strip(),
                    "Organization": organization.strip(),
                    "Location": location.strip(),
                    "URL": url
                })
        except Exception as e:
            print(f"Error retrieving job details: {e}")

    driver.quit()
    return jobs


def generate_csv(jobs, keyword):
    csv_file = f"{keyword}_apprenticeship_jobs.csv"
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Organization", "Location", "URL"])
        writer.writeheader()
        for job in jobs:
            writer.writerow(job)
    print(f"CSV generated: {csv_file}")
    return csv_file


if __name__ == "__main__":
    keyword = input("Enter the job keyword to search (e.g., 'data'): ")
    jobs = scrape_apprenticeship_site(keyword)

    if jobs:
        csv_file_path = generate_csv(jobs, keyword)
        print(f"CSV file is saved as: {csv_file_path}")
    else:
        print("No job listings found.")
