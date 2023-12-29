import requests
from bs4 import BeautifulSoup
import pandas as pd

# Replace with the actual URL containing the HTML
url = "https://collegedunia.com/india-colleges"
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.content, "html.parser")
# import pdb;pdb.set_trace()
cities = []
city_id = soup.find("div", id="city")
# .find("ul", class_="jsx-3159337366").text.strip().split(',')
for city_item in city_id.find_all("li"):
    checkbox = city_item.find("input", type="checkbox")
    city_id = checkbox["id"].split('-')[-1]
    city_name = city_item.find("label").text.strip().split('-')[0] 

    cities.append({"cityId": city_id, "cityName": city_name})

print(cities) 

city_dataframe = pd.DataFrame(cities)
city_dataframe.to_excel("city_data.xlsx", index=False)


# locations=city_id.find_all('li')  