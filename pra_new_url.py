import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import os

college_details = []

def extract_college_info(url):
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without a visible browser window)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    chrome_options.add_argument(f'user-agent={headers["User-Agent"]}')

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the college URL
    driver.get(url)

    # Get the updated page source after scrolling
    page_source = driver.page_source

    # Close the WebDriver
    driver.quit()

    # Parse the updated page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    college_divs = soup.find_all('div', class_='course-body')

    for i in college_divs:
        link =i.find('')
        name = i.find('div', class_='course-heading').find('a').find('h3').text.strip()
        # course_fees = i.find('div', class_='course-heading').find('div', class_='fees').find('span', class_='fee').text.strip() if i else 'Not Available'
        course_fees_element = i.find('div', class_='course-heading').find('div', class_='ml-auto')
        course_fees = course_fees_element.find().text.strip() if course_fees_element else 'Not Available'
        duration_of_cource = i.find('div', class_='course-info').find('div', class_='labels').find('span', class_='year').text.strip()
        degree = i.find('div', class_='course-info').find('div', class_='labels').find('span', class_='degree').text.strip()
        campus = i.find('div', class_='course-info').find('div', class_='labels').find().text.strip()
        graduation = i.find('div', class_='course-info').find('div', class_='labels').find().text.strip()
        types = i.find('div', class_='course-info').find('div', class_='labels').find('span', class_='type').text.strip()

        college_details.append({
            'Name': name,
            'Course Fees': course_fees,
            'Duration_of_cource': duration_of_cource,
            'Degree': degree,
            'Campus': campus,
            'Graduation': graduation,
            'Types': types,
            'Photos_URL': None,
            'Videos_URL': None,
        })
        
        # Extract and append photos and videos URLs
        gallery_url = url + "/gallery"
        driver.get(gallery_url)
        time.sleep(2)  # You might need to adjust the sleep duration

        gallery_page_source = driver.page_source
        gallery_soup = BeautifulSoup(gallery_page_source, 'html.parser')

        # Find the Campus section and get the URLs of photos and videos
        campus_section = gallery_soup.find('div', {'data-target': '#campus'})
        if campus_section:
            # Extract photos URL
            photos_url = campus_section.find('a', {'data-tab': '#photos'})
            if photos_url:
                college_details[-1]['Photos_URL'] = photos_url['href']

            # Extract videos URL
            videos_url = campus_section.find('a', {'data-tab': '#videos'})
            if videos_url:
                college_details[-1]['Videos_URL'] = videos_url['href']

    # # Create a DataFrame from the college details list
    # df = pd.DataFrame(college_details)

    # # Save the DataFrame to a JSON file
    # df.to_json('new_college_details_prac.json', orient='records', indent=2)
    # print("JSON file created successfully.")

    # # Save the DataFrame to an Excel file
    # df.to_excel('new_college_details_prac.xlsx', index=False)
    # print("Excel file created successfully.")

# Read the Excel file into a DataFrame

# excel_file_path = 'E:/Python-workspace/beautifulsoup_poc/practice_details3.xlsx'
excel_file_path = 'E:/Python-workspace/beautifulsoup_poc/practice_details3.xlsx'
df_links = pd.read_excel(excel_file_path)

# Iterate over each row in the DataFrame and call extract_college_info function
base_url="https://collegedunia.com"
tab_url = "/courses-fees"

for college_url in df_links['Link']:
    final_url = base_url + college_url + tab_url
    extract_college_info(final_url)
    print(final_url)
    
# Create a DataFrame from the college details list
df = pd.DataFrame(college_details)

# Specify the directory name
directory_name = 'College_Data_Files'
os.makedirs(directory_name, exist_ok=True)

# Save the DataFrame to a JSON file in the specified directory
# json_file_path = os.path.join(directory_name, 'College_Details.json')
json_file_path = os.path.join(directory_name, 'College_Details_1400.json')
df.to_json(json_file_path, orient='records', indent=2)
print("JSON file created successfully...")

# Save the DataFrame to an Excel file in the specified directory
# excel_file_path = os.path.join(directory_name, 'College_Details.xlsx')
excel_file_path = os.path.join(directory_name, 'College_Details_1400.xlsx')
df.to_excel(excel_file_path, index=False)
print("Excel file created successfully...")

# # Save the DataFrame to a JSON file
# df.to_json('College_Details.json', orient='records', indent=2)
# print("JSON file created successfully.")

# # Save the DataFrame to an Excel file
# df.to_excel('College_Details.xlsx', index=False)
# print("Excel file created successfully.")
