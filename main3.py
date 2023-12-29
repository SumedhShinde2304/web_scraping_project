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

urls = ["pune-colleges", "chennai-colleges", "mumbai-colleges", "gurgaon-colleges", "kolkata-colleges",
        "hyderabad-colleges", "bangalore-colleges", "ahmedabad-colleges", "noida-colleges", "noida-colleges",
        "lucknow-colleges", "bhopal-colleges", "jaipur-colleges", "coimbatore-colleges", "bhubaneswar-colleges",
        "indore-colleges", "indore-colleges","guntur-colleges","meerut-colleges","ghaziabad-colleges","greater-noida-colleges",
        "nagpur-colleges","mohali-colleges","tiruchirappalli-colleges","dehradun-colleges","visakhapatnam-colleges","kanpur-colleges",
        "kanpur-colleges","east-godavari-colleges","namakkal-colleges","thiruvananthapuram-colleges","gwalior-colleges",""]

base_url_be = "https://collegedunia.com/btech/computer-science/"
base_url_me = "https://collegedunia.com/mtech/computer-science/"

# Scrape BE/Btech and ME/Mtech concurrently
college_details = scrape_with_threadpool(base_url_be, urls, 'BE/Btech', 'computer-science') + \
                  scrape_with_threadpool(base_url_me, urls, 'ME/Mtech', 'computer-science')
# urls.append("pune-colleges")
# urls.append("chennai-colleges")
# urls.append("mumbai-colleges")
# urls.append("gurgaon-colleges")
# urls.append("kolkata-colleges")
# urls.append("hyderabad-colleges")
# urls.append("bangalore-colleges")
# urls.append("ahmedabad-colleges")
# urls.append("noida-colleges")
# urls.append("noida-colleges")
# urls.append("lucknow-colleges")
# urls.append("bhopal-colleges")
# urls.append("jaipur-colleges")
# urls.append("coimbatore-colleges")
# urls.append("bhubaneswar-colleges")
# urls.append("indore-colleges")
# urls.append("indore-colleges")




college_details=[]


# for sub_url in urls:
#     # import pdb;pdb.set_trace()
#     url = f"{base_url}{sub_url}"
#     print(f"triggering url {url}")
#     city =  url.split('/')[-1].split('-')[0]
#     college_detail={
#         'stream':'BE/Btech',
#         'subsream':'computer-science',
#         'city':city,
#         'url':url,
#     }
    
#     college_details.append(college_detail)
    
    
# for sub_url in urls:
#     # import pdb;pdb.set_trace()
#     url = f"{base_url}{sub_url}"
#     print(f"triggering url {url}")
#     city =  url.split('/')[-1].split('-')[0]
#     college_detail={
#         'stream':'ME/Mtech',
#         'subsream':'computer-science',
#         'city':city,
#         'url':url,
#     }
    
#     college_details.append(college_detail)
    
df = pd.DataFrame(college_details)

# Save the DataFrame to an Excel file
df.to_excel('college_details_for_practice2.xlsx', index=False)
print("Excel file created successfully.")


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

file_path = f'{sub_url}.html'
print(f"creating file.... {file_path}")
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(html_source)

print(f"HTML source has been saved to: {file_path}")
    
driver.quit()


