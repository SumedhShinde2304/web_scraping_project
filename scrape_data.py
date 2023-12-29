from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import os
import requests

def get_city_ids():
    print('get-city-ids...')
    url = "https://collegedunia.com/india-colleges"
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    cities = []
    city_id = soup.find("div", id="city")
    # .find("ul", class_="jsx-3159337366").text.strip().split(',')
    for city_item in city_id.find_all("li"):
        checkbox = city_item.find("input", type="checkbox")
        city_id = checkbox["id"].split('-')[-1]
        city_name = city_item.find("label").text.strip().split('-')[0] 

        cities.append({"cityName": city_name,"cityId": city_id})

    print(cities) 

    city_dataframe = pd.DataFrame(cities)
    city_dataframe.to_excel("city_data.xlsx", index=False)

get_city_ids()


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

# def scrape_with_threadpool(base_url, urls, stream, substream):
#     with ThreadPoolExecutor() as executor:
#         results = list(executor.map(lambda sub_url: scrape_url(base_url, sub_url, stream, substream), urls))
#         return results


# driver = webdriver.Chrome()
# urls = ["pune-colleges", "chennai-colleges", "mumbai-colleges", "gurgaon-colleges", "kolkata-colleges",
#         "hyderabad-colleges", "bangalore-colleges", "ahmedabad-colleges", "noida-colleges","raipur-colleges", 
#         "lucknow-colleges", "bhopal-colleges", "jaipur-colleges", "coimbatore-colleges", "bhubaneswar-colleges",
#         "indore-colleges", "indore-colleges", "guntur-colleges", "meerut-colleges", "ghaziabad-colleges",
#         "greater-noida-colleges", "nagpur-colleges", "mohali-colleges", "tiruchirappalli-colleges", "dehradun-colleges",
#         "visakhapatnam-colleges", "kanpur-colleges","east-godavari-colleges", "namakkal-colleges",
#         "thiruvananthapuram-colleges", "gwalior-colleges", "salem-colleges","bhilai-colleges","surat-colleges","jabalpur-colleges",
#         "kanchipuram-colleges","kanyakumari-colleges","nashik-colleges","faridabad-colleges","sonepat-colleges"," tirunelveli-colleges",
#         "allahabad-colleges"]
urls = ["pune-colleges", "chennai-colleges", "mumbai-colleges", "bangalore-colleges","kolkata-colleges"]


base_url_be = "https://collegedunia.com/btech/computer-science/"
base_url_me = "https://collegedunia.com/mtech/mechanical-engineering/"
base_url_bcom = "https://collegedunia.com/bcom/accounting/"
base_url_bsc = "https://collegedunia.com/bsc/physics/"

# Scrape BE/Btech and ME/Mtech concurrently
# college_details = [scrape_url(base_url_be, urls, 'BE/Btech', 'computer-science') +
#                   scrape_url(base_url_me, urls, 'ME/Mtech', 'chemical-engineering-colleges') +
#                   scrape_url(base_url_me, urls, 'B.Com', 'accounting-colleges') +
#                   scrape_url(base_url_me, urls, 'B.Sc', 'physics-colleges')]

college_details = [scrape_url(base_url_be, sub_url, 'BE/Btech', 'computer-science') for sub_url in urls] + \
                  [scrape_url(base_url_me, sub_url, 'ME/Mtech', 'mechanical-engineering') for sub_url in urls] + \
                  [scrape_url(base_url_bcom, sub_url, 'B.Com', 'accounting-colleges') for sub_url in urls] + \
                  [scrape_url(base_url_bsc, sub_url, 'B.Sc', 'physics-colleges') for sub_url in urls]


#
# Create DataFrame
# df = pd.DataFrame(college_details)

# Save the DataFrame to an Excel file
# df.to_excel('college_details_threads_practice1.xlsx', index=False)
# print("Excel file created successfully.")

read_file = pd.read_excel('college_details_threads_practice1.xlsx')
# print(read_file)
# read_file.show()


# #Group by 'stream'
# grouped = df.groupby(['stream'])
# for group in grouped:
#     print(group)



#Scraping HTML sources concurrently

def get_html_source(url):
    print('get_html_source...')
    driver = webdriver.Chrome()
    # import pdb;pdb.set_trace()
    start_time = time.time()
    # url = f"{base_url_be}{url}"
    driver.get(url)
    status_code = driver.execute_script("return window.fetch(arguments[0]).then(response => response.status);", driver.current_url)
    print(f'running url',url)
    
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
    
    #for stream folder
    stream_folder = url.split("/")[3]
    
    #for substream folder
    substream_folder = url.split("/")[4]  
  
    
    # Create directory structure if it doesn't exist
    directory_path = f'E:/Python-workspace/beautifulsoup_poc/html_sources/{stream_folder}/{substream_folder}'
    os.makedirs(directory_path, exist_ok=True)
    
    # Create the file path with dynamic folder structure
    file_path = f'{directory_path}/{url.split("/")[-1]}.html'
    
    print(f"creating file.... {file_path}")
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_source)

    print(f"HTML source has been saved to: {file_path}")
    
    end_time = time.time()

    complete_time = end_time - start_time

    print(f"Performance Time: {complete_time} seconds")
    driver.quit()
with ThreadPoolExecutor(max_workers=1) as executor:
    # Use list comprehension to submit tasks for each URL
    futures = [executor.submit(get_html_source, url) for url in read_file['url']] 


# driver.quit()

# # Process each group concurrently
# # with ThreadPoolExecutor() as executor:
# #     for group, group_df in grouped:
# #         urls_for_group = group_df['url'].tolist()
# #         executor.map(scrape_html_source, urls_for_group)



