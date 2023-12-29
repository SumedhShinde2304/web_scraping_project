import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import threading

college_details = []
lock = threading.Lock()

def scrape_page(i):
    link = i.find('div', class_='clg-name-address').find('a')['href']
    name = i.find('div', class_='clg-name-address').find('h3').text.strip()
    location = i.find('div', class_='clg-name-address').find('span', class_='location').text.strip().split(',')
    city = location[0]
    state = location[1]

    approvals_span = i.find('div', class_='clg-name-address').find('span', class_='approvals')
    approvals = approvals_span.text.replace('\xa0', ' ').strip() if approvals_span is not None else 'NA'
    course_fees = i.find('td', class_='col-fees').find('span').text.strip()
    courses_list = i.find('td', class_='col-fees').find_all('span')
    course_name = courses_list[2].text.strip()

    placement_td = i.find('td', class_='col-placement')
    if placement_td:
        placements = placement_td.find_all('span', class_='jsx-914129990')
        if placements and len(placements) >= 3:
            avg_placement = placements[0].text.replace('\xa0', '').strip()
            highest_placement = placements[2].text.replace('\xa0', '').strip()
        else:
            avg_placement = 'NA'
            highest_placement = placements[0].text.replace('\xa0', '').strip()
    else:
        avg_placement = 'NA'
        highest_placement = 'NA'

    return {
        'Link': link,
        'College Name': name,
        'City': city,
        'State': state,
        'Approvals': approvals,
        'Course Fees': course_fees,
        'Course Name': course_name,
        'Average Placement': avg_placement,
        'Highest Placement': highest_placement,
    }

def get_college_info(num_of_scroll):
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without a visible browser window)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    chrome_options.add_argument(f'user-agent={headers["User-Agent"]}')

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the website
    base_url = 'https://collegedunia.com/india-colleges'
    driver.get(base_url)

    for _ in range(num_of_scroll):
        print("scrolling")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2.5)  # Adjust the sleep duration as needed

        # Get the updated page source after scrolling
        page_source = driver.page_source

        # Parse the updated page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        college_divs = soup.find_all('tbody', class_='jsx-2796823646')

        # Perform scraping in multiple threads
        threads = []
        for i in college_divs:
            thread = threading.Thread(target=lambda x: process_college_data(scrape_page(x)), args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all scraping threads to finish
        for thread in threads:
            thread.join()

    # Close the WebDriver
    driver.quit()

    # Create a DataFrame from the college details list
    df = pd.DataFrame(college_details)

    # Save the DataFrame to a JSON file
    df.to_json('practice_details3.json', orient='records', indent=2)
    print("JSON file created successfully.")

    # Save the DataFrame to an Excel file
    df.to_excel('practice_details3.xlsx', index=False)
    print("Excel file created successfully.")

def process_college_data(data):
    with lock:
        college_details.append(data)

get_college_info(5)
