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

urls = ["pune-colleges", "chennai-colleges", "mumbai-colleges", "bangalore-colleges","kolkata-colleges"]


base_url_be = "https://collegedunia.com/btech/computer-science/"
base_url_me = "https://collegedunia.com/mtech/mechanical-engineering/"
base_url_bcom = "https://collegedunia.com/bcom/accounting/"
base_url_bsc = "https://collegedunia.com/bsc/physics/"


college_details = [scrape_url(base_url_be, sub_url, 'BE/Btech', 'computer-science') for sub_url in urls] + \
                  [scrape_url(base_url_me, sub_url, 'ME/Mtech', 'mechanical-engineering') for sub_url in urls] + \
                  [scrape_url(base_url_bcom, sub_url, 'B.Com', 'accounting-colleges') for sub_url in urls] + \
                  [scrape_url(base_url_bsc, sub_url, 'B.Sc', 'physics-colleges') for sub_url in urls]


#
# Create DataFrame
df = pd.DataFrame(college_details)

# Save the DataFrame to an Excel file
df.to_excel('college_details_threads_practice1.xlsx', index=False)
print("Excel file created successfully.")

read_file = pd.read_excel('college_details_threads_practice1.xlsx')
# print(read_file)
# read_file.show()


# #Group by 'stream'
# grouped = df.groupby(['stream'])
# for group in grouped:
#     print(group)

def get_html_source(url):
    driver = webdriver.Chrome()
    start_time = time.time()
    driver.get(url)
    print(f'running url', url)
    
    scroll_pause_time = 1  # Pause between each scroll
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
    
    # Extract city ID from the URL
    city_id = 344
    if "?city_id=" in url:
        city_id = url.split("?city_id=")[-1]

    # For stream folder
    stream_folder = url.split("/")[3]
    
    # For substream folder
    substream_folder = url.split("/")[4]  

    # Create directory structure if it doesn't exist
    directory_path = f'E:/Python-workspace/beautifulsoup_poc/html_sources/{stream_folder}/{substream_folder}'
    os.makedirs(directory_path, exist_ok=True)
    
    # Create the file path with dynamic folder structure
    if city_id:
        file_path = f'{directory_path}/{city_id}.html'
    else:
        file_path = f'{directory_path}/{url.split("/")[-1]}.html'
    
    print(f"creating file.... {file_path}")
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_source)

    print(f"HTML source has been saved to: {file_path}")
    
    end_time = time.time()
    complete_time = end_time - start_time

    print(f"Performance Time: {complete_time} seconds")
    driver.quit()
    
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(get_html_source, url) for url in read_file['url']]

