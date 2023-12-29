from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

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

def scrape_with_threadpool(base_url, urls, stream, substream):
    with ThreadPoolExecutor() as executor:
        return list(executor.map(lambda sub_url: scrape_url(base_url, sub_url, stream, substream), urls))

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
urls = ["pune-colleges", "chennai-colleges", "mumbai-colleges", "bangalore-colleges", "indore-colleges"]


# base_url_be = "https://collegedunia.com/btech/computer-science/"
# base_url_me = "https://collegedunia.com/mtech/computer-science/"
# base_url_me = "https://collegedunia.com/bcom-colleges/"
# base_url_me = "https://collegedunia.com/bsc-colleges/"

# # Scrape BE/Btech and ME/Mtech concurrently
# college_details = [scrape_url(base_url_be, urls, 'BE/Btech', 'computer-science') + \
#                   scrape_url(base_url_me, urls, 'ME/Mtech', 'chemical-engineering-colleges') + \
#                   scrape_url(base_url_me, urls, 'B.Com', 'accounting-colleges') + \
#                   scrape_url(base_url_me, urls, 'B.Sc', 'physics-colleges')  ]


base_url_be = "https://collegedunia.com/btech/computer-science/"
base_url_me = "https://collegedunia.com/mtech/computer-science/"
base_url_bcom = "https://collegedunia.com/bcom-colleges/"
base_url_bsc = "https://collegedunia.com/bsc-colleges/"

# Scrape BE/Btech and ME/Mtech concurrently
college_details = scrape_with_threadpool(base_url_be, urls, 'BE/Btech', 'computer-science') + \
                  scrape_with_threadpool(base_url_me, urls, 'ME/Mtech', 'chemical-engineering-colleges') + \
                  scrape_with_threadpool(base_url_bcom, urls, 'B.Com', 'accounting-colleges') + \
                  scrape_with_threadpool(base_url_bsc, urls, 'B.Sc', 'physics-colleges')

# Create DataFrame
df = pd.DataFrame(college_details)

# Save the DataFrame to an Excel file
df.to_excel('college_details_for_practice3.xlsx', index=False)
print("Excel file created successfully.")

# Scraping HTML sources concurrently
# def scrape_html_source(sub_url):
#     url = f"{base_url_be}{sub_url}"
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

#     file_path = f'{sub_url}.html'
#     print(f"creating file.... {file_path}")
#     with open(file_path, 'w', encoding='utf-8') as file:
#         file.write(html_source)

#     print(f"HTML source has been saved to: {file_path}")

# # Scrape HTML sources concurrently
# with ThreadPoolExecutor() as executor:
#     executor.map(scrape_html_source, urls)

# driver.quit()


