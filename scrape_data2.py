from bs4 import BeautifulSoup
from selenium import webdriver
import time

driver = webdriver.Chrome() 

urls = []
base_url = "https://collegedunia.com/btech/computer-science/"
urls.append("pune-colleges")
urls.append("chennai-colleges")

for sub_url in urls:
    url = f"{base_url}{sub_url}"
    print(f"triggering url {url}")
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