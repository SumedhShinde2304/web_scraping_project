from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import os
import requests
from urllib.parse import parse_qs, urlparse

def get_city_ids():
    print('get-city-ids...')
    url = "https://collegedunia.com/india-colleges"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    cities = []
    city_id = soup.find("div", id="city")

    for city_item in city_id.find_all("li"):
        checkbox = city_item.find("input", type="checkbox")
        city_id = checkbox["id"].split('-')[-1]
        city_name = city_item.find("label").text.strip().split('-')[0]
        cities.append({"cityName": city_name, "cityId": city_id})

    city_dataframe = pd.DataFrame(cities)
    city_dataframe.to_excel("city_data.xlsx", index=False)
    return city_dataframe

def scrape_html_for_city(city_row, base_url, stream):
    city_name = city_row["cityName"]
    city_id = city_row["cityId"]
    
    # Construct the URL dynamically
    url = f"{base_url}{stream}/city_id={city_id}"

    print(f"Scraping HTML source for {city_name} - {url}")

    stream_folder = url.split("/")[3]
    substream_folder = url.split("/")[4]

    directory_path = f'E:/Python-workspace/beautifulsoup_poc/html_sources/{stream_folder}/{substream_folder}'
    os.makedirs(directory_path, exist_ok=True)

    file_path = f'{directory_path}/{city_name}.html'

    driver = webdriver.Chrome()
    driver.get(url)

    scroll_pause_time = 1
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1
    while True:
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        time.sleep(scroll_pause_time)

        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if screen_height * i > scroll_height:
            break

    soup = BeautifulSoup(driver.page_source, "html.parser")
    html_source = soup.prettify()

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_source)

    print(f"HTML source has been saved to: {file_path}")

    driver.quit()

def scrape_url(base_url, sub_url, stream, substream):
    url = f"{base_url}{sub_url}"
    print(f"triggering url {url}")
    city = url.split('/')[-1].split('-')[0]
    college_detail = {
        'stream': stream,
        'substream': substream,
        'city': city,
        'url': url,
    }
    return college_detail

# Your existing code
base_url_be = "https://collegedunia.com/btech/computer-science/"
base_url_me = "https://collegedunia.com/mtech/mechanical-engineering/"
base_url_bcom = "https://collegedunia.com/bcom/accounting/"
base_url_bsc = "https://collegedunia.com/bsc/physics/"

# Specify the streams for which you want to scrape HTML sources
streams_to_scrape = ['computer-science', 'mechanical-engineering', 'accounting-colleges', 'physics-colleges']  # Add or remove streams as needed

# Get city names and IDs
city_df = get_city_ids()

if city_df is not None:
    # Use ThreadPoolExecutor to scrape HTML sources for each city and stream concurrently
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for stream_to_scrape in streams_to_scrape:
            futures.extend([executor.submit(scrape_html_for_city, row, base_url_bcom, stream_to_scrape) for index, row in city_df.iterrows()])
else:
    print("Failed to fetch city data.")
