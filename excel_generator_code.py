from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import os


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


driver = webdriver.Chrome()


urls = ["pune-colleges", "chennai-colleges", "mumbai-colleges", "bangalore-colleges", "kolkata-colleges"]


base_url_be = "https://collegedunia.com/btech/computer-science/"
base_url_me = "https://collegedunia.com/mtech/chemical-engineering-colleges/"
base_url_me = "https://collegedunia.com/bcom/accounting/"
base_url_me = "https://collegedunia.com/bsc/physics/"


college_details = [scrape_url(base_url_be, sub_url, 'BE/Btech', 'computer-science') for sub_url in urls] + \
                  [scrape_url(base_url_me, sub_url, 'ME/Mtech', 'chemical-engineering-colleges') for sub_url in urls] + \
                  [scrape_url(base_url_me, sub_url, 'B.Com', 'accounting-colleges') for sub_url in urls] + \
                  [scrape_url(base_url_me, sub_url, 'B.Sc', 'physics-colleges') for sub_url in urls]


# import pdb;pdb.set_trace()
# Create DataFrame
df = pd.DataFrame(college_details)

# Save the DataFrame to an Excel file
df.to_excel('college_details_threads_practice12.xlsx', index=False)
print("Excel file created successfully.")

# Scraping HTML sources concurrently333
def scrape_html_source(sub_url):
    url = f"{base_url_be}{sub_url}"
    print("===========",url)
    driver.get(url)

    scroll_pause_time = 1  # Pause between each scroll
    screen_height = driver.execute_script("return window.screen.height;")  # Browser window height
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
    
    # stream_folder = os.path.join("html_sources", group)
    # os.makedirs(stream_folder, exist_ok=True)

    # substream_folder = os.path.join(stream_folder, sub_url.split('-')[-1])
    # os.makedirs(substream_folder, exist_ok=True)
    
    file_path = f'{sub_url}.html'
    print(f"creating file.... {file_path}")
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_source)

    print(f"HTML source has been saved to: {file_path}")

# Scrape HTML sources concurrently
with ThreadPoolExecutor() as executor:
    executor.map(scrape_html_source, urls)

driver.quit()