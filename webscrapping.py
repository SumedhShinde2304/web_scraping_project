import requests
from bs4 import BeautifulSoup
import pandas as pd

car_details = []
def get_used_car_info():
    list_of_urls = ['https://www.cars24.com/buy-used-car?f=make%3A%3D%3Atata&sort=bestmatch&serveWarrantyCount=true&listingSource=Homepage_Filters&storeCityId=2&pinId=110001','https://www.cars24.com/buy-used-car?f=make%3A%3D%3Ahyundai&sort=bestmatch&serveWarrantyCount=true&gaId=1822748221.1701951734&listingSource=Homepage_Filters&storeCityId=2920&pinId=450001',
    'https://www.cars24.com/buy-used-car?f=make%3A%3D%3Ahyundai%3Bmodel%3Ain%3Anew%20santro%2Ci20%2Ci10%2Ccreta%2Cgrand%20i10%20nios%2Csantro%20xing%2Cxcent%2Cverna%2Ci20%20active%2Cnew%20i20%2Cnew%20elantra%2Csonata%2Cnew%20i20%20n%20line%2Cxcent%20prime%2Cgrand%20i10%20prime%2Calcazar%2Caccent%2Cvenue%2Caura%2Ctucson%20new%3AOR%3Amake%3A%3D%3Arenault&sort=bestmatch&serveWarrantyCount=true&gaId=1822748221.1701951734&listingSource=TabFilter&storeCityId=6356&pinId=682001',
    'https://www.cars24.com/buy-used-car?f=make%3A%3D%3Ahyundai%3Bmodel%3Ain%3Anew%20santro%2Ci20%2Ci10%2Ccreta%2Cgrand%20i10%20nios%2Csantro%20xing%2Cxcent%2Cverna%2Ci20%20active%2Cnew%20i20%2Cnew%20elantra%2Csonata%2Cnew%20i20%20n%20line%2Cxcent%20prime%2Cgrand%20i10%20prime%2Calcazar%2Caccent%2Cvenue%2Caura%2Ctucson%20new%3AOR%3Amake%3A%3D%3Arenault&sort=bestmatch&serveWarrantyCount=true&gaId=1822748221.1701951734&storeCityId=2423&pinId=411001',
    'https://www.cars24.com/buy-used-car?f=make%3A%3D%3Ahyundai%3Bmodel%3Ain%3Anew%20santro%2Ci20%2Ci10%2Ccreta%2Cgrand%20i10%20nios%2Csantro%20xing%2Cxcent%2Cverna%2Ci20%20active%2Cnew%20i20%2Cnew%20elantra%2Csonata%2Cnew%20i20%20n%20line%2Cxcent%20prime%2Cgrand%20i10%20prime%2Calcazar%2Caccent%2Cvenue%2Caura%2Ctucson%20new%3AOR%3Amake%3A%3D%3Arenault&sort=bestmatch&serveWarrantyCount=true&gaId=1822748221.1701951734&storeCityId=33&pinId=124001']
    for base_url in list_of_urls:
        base_url = f'{base_url}'
        # https://www.cars24.com/buy-used-car?f=make%3A%3D%3Ahyundai&sort=bestmatch&serveWarrantyCount=true&gaId=1822748221.1701951734&listingSource=Homepage_Filters&storeCityId=2920&pinId=450001
        # 'https://www.carwale.com/used/cars-in-pune/?pn=1&kms=0-&year=0-&budget=0-&city=12&state=-1&car=16&so=-1&sc=-1'
        # 'https://www.carwale.com/used/cars-in-pune/'
        # response = requests.get(base_url)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            car_info_elements = soup.find_all('div', class_='_2z-Yu')
            for car_div in car_info_elements:
                title = car_div.find('h3', class_='_2lmIw').text.strip()
                transmission = car_div.select_one('ul._1hOnS li:not(._1aIyR)').text.strip()
                km = car_div.select_one('ul._13yb6 li:nth-of-type(1)').text.strip()
                price = car_div.select_one('div._18ToE span').text.strip()

                car_details.append({
                'Carmodel': title,
                'Transmission': transmission,
                'Kilometers': km,
                'Price': price,
                })

    # Create a DataFrame from the car details list
    df = pd.DataFrame(car_details)

    # Save the DataFrame to an Excel file
    df.to_excel('car_details_using_bsoup.xlsx', index=False)

    print("Excel file created successfully.")

get_used_car_info()