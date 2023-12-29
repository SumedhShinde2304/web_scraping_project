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

# def scrape_with_threadpool(base_url, urls, stream, substream):
#     with ThreadPoolExecutor() as executor:
#         results = list(executor.map(lambda sub_url: scrape_url(base_url, sub_url, stream, substream), urls))
#         return results


driver = webdriver.Chrome()
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
# base_url_bcom = "https://collegedunia.com/bcom/accounting/"
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
# import pdb;pdb.set_trace()
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
    # import pdb;pdb.set_trace()
    start_time = time.time()
    # url = f"{base_url_be}{url}"
    driver.get(url)
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

with ThreadPoolExecutor(max_workers=3) as executor:
    # Use list comprehension to submit tasks for each URL
    futures = [executor.submit(get_html_source, url) for url in read_file['url']] #url chya jagi url karayach ahe
    

driver.quit()

# # Process each group concurrently
# # with ThreadPoolExecutor() as executor:
# #     for group, group_df in grouped:
# #         urls_for_group = group_df['url'].tolist()
# #         executor.map(scrape_html_source, urls_for_group)































# from bs4 import BeautifulSoup
# from selenium import webdriver
# import time
# import pandas as pd
# from concurrent.futures import ThreadPoolExecutor
# import os


# def scrape_url(base_url, sub_url, stream, substream):
#     url = f"{base_url}{sub_url}"
#     print(f"triggering url {url}")
#     city = url.split('/')[-1].split('-')[0]
#     college_detail = {
#         'stream': stream,
#         'substream': substream,
#         'city': city,
#         'url': url,
#     }
#     return college_detail

# def scrape_with_threadpool(base_url, urls, stream, substream):
#     with ThreadPoolExecutor() as executor:
#         results = list(executor.map(lambda sub_url: scrape_url(base_url, sub_url, stream, substream), urls))
#         return results


# driver = webdriver.Chrome()
# # urls = ["pune-colleges", "chennai-colleges", "mumbai-colleges", "gurgaon-colleges", "kolkata-colleges",
# #         "hyderabad-colleges", "bangalore-colleges", "ahmedabad-colleges", "noida-colleges","raipur-colleges", 
# #         "lucknow-colleges", "bhopal-colleges", "jaipur-colleges", "coimbatore-colleges", "bhubaneswar-colleges",
# #         "indore-colleges", "indore-colleges", "guntur-colleges", "meerut-colleges", "ghaziabad-colleges",
# #         "greater-noida-colleges", "nagpur-colleges", "mohali-colleges", "tiruchirappalli-colleges", "dehradun-colleges",
# #         "visakhapatnam-colleges", "kanpur-colleges","east-godavari-colleges", "namakkal-colleges",
# #         "thiruvananthapuram-colleges", "gwalior-colleges", "salem-colleges","bhilai-colleges","surat-colleges","jabalpur-colleges",
# #         "kanchipuram-colleges","kanyakumari-colleges","nashik-colleges","faridabad-colleges","sonepat-colleges"," tirunelveli-colleges",
# #         "allahabad-colleges"]
# urls = ["pune-colleges", "chennai-colleges", "mumbai-colleges", "bangalore-colleges", "indore-colleges"]


# base_urls = {
#     'BE/Btech': "https://collegedunia.com/btech/",
#     'ME/Mtech': "https://collegedunia.com/mtech/",
#     'B.Com': "https://collegedunia.com/bcom/",
#     'B.Sc': "https://collegedunia.com/bsc/"
# }

# # Scrape BE/Btech and ME/Mtech concurrently
# college_details = [
#     *scrape_with_threadpool(base_urls, urls, 'BE/Btech', 'computer-science'),
#     *scrape_with_threadpool(base_urls, urls, 'ME/Mtech', 'chemical-engineering-colleges'),
#     *scrape_with_threadpool(base_urls, urls, 'B.Com', 'accounting-colleges'),
#     *scrape_with_threadpool(base_urls, urls, 'B.Sc', 'physics-colleges')
# ]
# # import pdb;pdb.set_trace()
# # Create DataFrame
# df = pd.DataFrame(college_details)

# # Save the DataFrame to an Excel file
# df.to_excel('college_details_threads_practice1.xlsx', index=False)
# print("Excel file created successfully.")


# # Group by 'stream'
# grouped = df.groupby(['stream'])
# for group in grouped:
#     print(group)



# # Scraping HTML sources concurrently
# def scrape_html_source(sub_url):
#     url = f"{base_urls}{sub_url}"
#     driver.get(url)

#     scroll_pause_time = 1  # Pause between each scroll
#     screen_height = driver.execute_script("return window.screen.height;")  # Browser window height
#     i = 1
#     while True:
#         driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
#         i += 1
#         time.sleep(scroll_pause_time)

#         scroll_height = driver.execute_script("return document.body.scrollHeight;")
#         if screen_height * i > scroll_height:
#             break

#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     html_source = soup.prettify()
    
#     stream_folder = os.path.join("html_sources", group)
#     os.makedirs(stream_folder, exist_ok=True)

#     substream_folder = os.path.join(stream_folder, sub_url.split('-')[-1])
#     os.makedirs(substream_folder, exist_ok=True)
    
#     file_path = f'{sub_url}.html'
#     print(f"creating file.... {file_path}")
#     with open(file_path, 'w', encoding='utf-8') as file:
#         file.write(html_source)

#     print(f"HTML source has been saved to: {file_path}")

# # Scrape HTML sources concurrently
# with ThreadPoolExecutor() as executor:
#     executor.map(scrape_html_source, urls)

# driver.quit()

# # Process each group concurrently
# with ThreadPoolExecutor() as executor:
#     for group, group_df in grouped:
#         urls_for_group = group_df['url'].tolist()
#         executor.map(scrape_html_source, urls_for_group)





















# from bs4 import BeautifulSoup
# from selenium import webdriver
# import time
# import pandas as pd
# from concurrent.futures import ThreadPoolExecutor
# import os

# def scrape_url(base_url, sub_url, stream, substream):
#         return college_detail

# def scrape_with_threadpool(base_url, urls, stream, substream):
#     with ThreadPoolExecutor() as executor:
#         results = list(executor.map(lambda sub_url: scrape_url(base_url, sub_url, stream, substream), urls))
#         return results

# def scrape_html_source(sub_url):
#     url = f"{base_urls}{sub_url}"
#     driver.get(url)

#     scroll_pause_time = 1  # Pause between each scroll
#     screen_height = driver.execute_script("return window.screen.height;")  # Browser window height
#     i = 1
#     while True:
#         driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
#         i += 1
#         time.sleep(scroll_pause_time)

#         scroll_height = driver.execute_script("return document.body.scrollHeight;")
#         if screen_height * i > scroll_height:
#             break

#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     html_source = soup.prettify()
    
#     stream_folder = os.path.join("html_sources", group)
#     os.makedirs(stream_folder, exist_ok=True)

#     substream_folder = os.path.join(stream_folder, sub_url.split('-')[-1])
#     os.makedirs(substream_folder, exist_ok=True)
    
#     file_path = f'{sub_url}.html'
#     print(f"creating file.... {file_path}")
#     with open(file_path, 'w', encoding='utf-8') as file:
#         file.write(html_source)

#     print(f"HTML source has been saved to: {file_path}")

# driver = webdriver.Chrome()

# urls = ["pune-colleges", "chennai-colleges", "mumbai-colleges", "bangalore-colleges", "indore-colleges"]

# base_urls = {
#     'BE/Btech': "https://collegedunia.com/btech/",
#     'ME/Mtech': "https://collegedunia.com/mtech/",
#     'B.Com': "https://collegedunia.com/bcom/",
#     'B.Sc': "https://collegedunia.com/bsc/"
# }

# # Scrape BE/Btech and ME/Mtech concurrently
# college_details = [
#     *scrape_with_threadpool(base_urls, urls, 'BE/Btech', 'computer-science'),
#     *scrape_with_threadpool(base_urls, urls, 'ME/Mtech', 'chemical-engineering-colleges'),
#     *scrape_with_threadpool(base_urls, urls, 'B.Com', 'accounting-colleges'),
#     *scrape_with_threadpool(base_urls, urls, 'B.Sc', 'physics-colleges')
# ]

# # Create DataFrame
# df = pd.DataFrame(college_details)

# # Save the DataFrame to an Excel file
# df.to_excel('college_details_threads_practice1.xlsx', index=False)
# print("Excel file created successfully.")

# # Group by 'stream'
# grouped = df.groupby(['stream'])

# # Process each group concurrently
# with ThreadPoolExecutor() as executor:
#     for group, group_df in grouped:
#         urls_for_group = group_df['url'].tolist()
#         executor.map(scrape_html_source, urls_for_group)

# driver.quit()url = f"{base_url}{sub_url}"
#     print(f"triggering url {url}")
#     city = url.split('/')[-1].split('-')[0]
#     college_detail = {
#         'stream': stream,
#         'substream': substream,
#         'city': city,
#         'url': url,
#     }

