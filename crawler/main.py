
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

import requests
import csv
import os



# Defining function to get a list of busiest airports by international passenger traffic in 2022 from wiki
wiki_url = "https://en.wikipedia.org/wiki/List_of_busiest_airports_by_international_passenger_traffic"
busiest_airports_result = []

def get_busiest_airports():
    try:
        cookies = {
    'WMF-Last-Access': '20-Dec-2023',
    'WMF-Last-Access-Global': '20-Dec-2023',
    'GeoIP': 'LT:VL:Vilnius:54.69:25.28:v4',
    'NetworkProbeLimit': '0.001',
    'enwikimwuser-sessionId': 'f4f436c6421f45df0163',
    'WMF-DP': 'bee,007,e43,872,3a6',
}
        headers = {
    'authority': 'en.wikipedia.org',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    #'cookie': 'WMF-Last-Access=20-Dec-2023; WMF-Last-Access-Global=20-Dec-2023; GeoIP=LT:VL:Vilnius:54.69:25.28:v4; NetworkProbeLimit=0.001; enwikimwuser-sessionId=f4f436c6421f45df0163; WMF-DP=bee,007,e43,872,3a6',
    #'if-modified-since': 'Tue, 19 Dec 2023 01:19:25 GMT',
    'referer': 'https://www.bing.com/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
}
        response = requests.get(wiki_url, cookies=cookies, headers=headers,)
        response.raise_for_status()
        #print(response.status_code)
        #print(response)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            #print(soup)
            table = soup.find('table', {'class': 'wikitable'})
            #print(table)
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td'])
                    if cells and len(cells) >= 3:
                        city = cells[1].text.strip()
                        airport_name = cells[2].text.strip()
                        airport_code = cells[4].text.strip()
                        passengers = cells[5].text.strip()
                        airport_code_split = airport_code.split('/')[0]
                        busiest_airports_result.append({
                            'City': city,
                            'Airport': airport_name,
                            'Airport Code': airport_code_split,
                            'Passengers': passengers
                        })
                        #print(f"City: {city}, Airport: {airport_name}, Airport Code: {airport_code}, Passengers: {passengers}")
            else:
                print("Table not found on the page.")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


get_busiest_airports()
print(busiest_airports_result)



# Defining save to csv function to save dictionary of busiest airports data gathered with 'get_busiest_airports' function
def save_to_csv(data, folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


sample_data_folder = 'sample data'
file_name = 'busiest_airports_result.csv'

# Save the data to a CSV file in the 'sample data' folder
# save_to_csv(busiest_airports_result, sample_data_folder, file_name)


# Function example to create url's for further data gathering according the list created with 'get_busiest_airports' function
# def get_city_data(cities_data):
#     for city_info in cities_data:
#         city_code = city_info.get('Airport Code')
#         if city_code:
#             city_data = {"City Code": city_code, "General Info": None, "Arrivals": None, "Departures": None}

#             try:
#                 # General Info
#                 general_url = f"https://www.flightradar24.com/data/airports/{city_code}"
#                 general_response = requests.get(general_url)
#                 general_response.raise_for_status()
#                 general_soup = BeautifulSoup(general_response.content, 'html.parser')
#                 city_data["General Info"] = general_soup  # Store general information, modify as needed

#                 # Arrivals
#                 arrivals_url = f"https://www.flightradar24.com/data/airports/{city_code}/arrivals"
#                 arrivals_response = requests.get(arrivals_url)
#                 arrivals_response.raise_for_status()
#                 arrivals_soup = BeautifulSoup(arrivals_response.content, 'html.parser')
#                 city_data["Arrivals"] = arrivals_soup  # Store arrivals information, modify as needed

#                 # Departures
#                 departures_url = f"https://www.flightradar24.com/data/airports/{city_code}/departures"
#                 departures_response = requests.get(departures_url)
#                 departures_response.raise_for_status()
#                 departures_soup = BeautifulSoup(departures_response.content, 'html.parser')
#                 city_data["Departures"] = departures_soup  # Store departures information, modify as needed

#             except Exception as e:
#                 print(f"An error occurred for {city_code}: {e}")

#             # Process or store city_data as needed
#             print(city_data)

# # Example usage with your provided dictionary
# city_info_list = [{'City': 'Dubai', 'Airport': 'Dubai International Airport', 'Airport Code': 'DXB', 'Passengers': '66,069,981'}, {'City': 'London', 'Airport': 'London Heathrow Airport', 'Airport Code': 'LHR', 'Passengers': '58,243,060'}, {'City': 'Amsterdam', 'Airport': 'Amsterdam Airport Schiphol', 'Airport Code': 'AMS', 'Passengers': '52,467,346'}, {'City': 'Paris', 'Airport': 'Paris-Charles de Gaulle Airport', 'Airport Code': 'CDG', 'Passengers': '51,763,569'}, {'City': 'Istanbul', 'Airport': 'Istanbul Airport', 'Airport Code': 'IST', 'Passengers': '48,521,725'}, {'City': 'Frankfurt', 'Airport': 'Frankfurt Airport', 'Airport Code': 'FRA', 'Passengers': '44,771,711'}, {'City': 'Madrid', 'Airport': 'Madrid-Barajas Airport', 'Airport Code': 'MAD', 'Passengers': '36,231,191'}, {'City': 'Doha', 'Airport': 'Hamad International Airport', 'Airport Code': 'DOH', 'Passengers': '35,726,721'}, {'City': 'Singapore', 'Airport': 'Singapore Changi Airport', 'Airport Code': 'SIN', 'Passengers': '31,902,000'}, {'City': 'London', 'Airport': 'London Gatwick Airport', 'Airport Code': 'LGW', 'Passengers': '30,145,083'}]

# get_city_data(city_info_list)









# Defining function to get data of busiest airports found in previous function from another website
#fr_url = "https://www.flightradar24.com/data/airports"

# def get_airports_data():
#     try:
#         cookies = {
#     '__cfruid': 'eedb0dee08799d4b8137afb19826cfd8a9cfee10-1703090952',
#     '_ga': 'GA1.1.2073150740.1703090953',
#     'OptanonAlertBoxClosed': '2023-12-20T16:49:13.195Z',
#     'eupubconsent-v2': 'CP3FLfAP3FLfAAcABBENAfEsAP_gAEPgAAYgg1NX_H__bW9r8Xr3aft0eY1P99j77sQxBhfJE-4FyLvW_JwXx2EwNA26tqIKmRIEu3ZBIQFlHJHURVigaogVryHsYkGcgTNKJ6BkgFMRM2dYCF5vmYtj-QKY5_p9d3fx2D-t_dv83dzzz8VHn3e5fmckcICdQ58tDfn9bRKb-5IOd_78v4v09F_rk2_eTVn_pcvr7B-uft87_XU-9_feAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQagCzDQqIA-yJCQi0HCKBACIKwgIoEAAAAJA0QEAJAwKdgYBLrCRACBFAAMEAIAAUZAAgAAEgAQiACQAoEAAEAgEAAAAAAgEADAwADgAtBAIAAQHQMUwoAFAsIEjMiIUwIQoEggJbKBBICgQVwgCLHAigERMFAAgCQAVgAAAsVgMQSAlYkECWEG0AABAAgFFKFQik6MAQwJmy1U4om0ZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAACAA.f_wACHwAAAAA',
#     '_cc_id': 'a5350f40adf077346e2ddfbc3945f34f',
#     'panoramaId_expiry': '1703695755003',
#     'panoramaId': 'f2dca077afece39eea354494d2fe185ca02c4c5af4b316b5a480cc2049bb8161',
#     'panoramaIdType': 'panoDevice',
#     '__gads': 'ID=2854876d02e39999:T=1703090954:RT=1703090954:S=ALNI_MZgvj694RiOqmUkEv98XpZE7hLPDA',
#     '__gpi': 'UID=00000d24162c7afb:T=1703090954:RT=1703090954:S=ALNI_Ma7vkJu1-ObIR40_IBIKhlc-2V0tg',
#     'OptanonConsent': 'isGpcEnabled=0&datestamp=Wed+Dec+20+2023+18%3A52%3A55+GMT%2B0200+(Eastern+European+Standard+Time)&version=202311.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5787432d-8422-4227-a270-e88ceb3d760f&interactionCount=1&landingPath=NotLandingPage&groups=C0002%3A1%2CC0001%3A1%2CC0004%3A1%2CC0003%3A1%2CV2STACK42%3A1&geolocation=LT%3BVL&AwaitingReconsent=false',
#     'cto_bundle': 'i3SioV9HWUdtRVp0cDdaJTJGT3RSd0ZISFR4UjFqcmtFMGVDcnZOblNiMjNCZDBrUWUlMkJpR0FTVVE0a1BNOHlEcHBLJTJCY0pYR2NCOHpKRm1RRG5RUHJpVTRvSTlUc082Sk9mOGZpYjJnY2M4a09vJTJCeU9sc1d1a1JXOFp2YmFFeGxBODJjNldMejdVMldIZnhqRGZSUVBtREZzdzROdyUzRCUzRA',
#     'mp_942a098c72ecbdd6c0d9c00fe8308319_mixpanel': '%7B%22distinct_id%22%3A%20%2218c882199e624a-034b25690e05f4-4c657b58-144000-18c882199e712fe%22%2C%22%24device_id%22%3A%20%2218c882199e624a-034b25690e05f4-4c657b58-144000-18c882199e712fe%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D',
#     'FCNEC': '%5B%5B%22AKsRol9L6lnJOoEbbQFDhaHHGz6Vu0FXO-vEoYOjcPOqqlzk-Yd3KCHEF1ciCRuxR0btr9dLGEtx9FzfrYftLlQJ0epAJ-f0hO_2p8KUZdyIzV0Ew7v-AZhbDCNzM_7toQ6euiCKs-kgiSFcv1juOhpsKKzQ5NK1VQ%3D%3D%22%5D%2Cnull%2C%5B%5B5%2C%22226%22%5D%5D%5D',
#     '_ga_38V2BZ2HMF': 'GS1.1.1703090952.1.1.1703091188.48.0.0',
# }
#         headers = {
#     'authority': 'www.flightradar24.com',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'accept-language': 'en-US,en;q=0.9',
#     'cache-control': 'max-age=0',
#     #'cookie': '__cfruid=eedb0dee08799d4b8137afb19826cfd8a9cfee10-1703090952; _ga=GA1.1.2073150740.1703090953; OptanonAlertBoxClosed=2023-12-20T16:49:13.195Z; eupubconsent-v2=CP3FLfAP3FLfAAcABBENAfEsAP_gAEPgAAYgg1NX_H__bW9r8Xr3aft0eY1P99j77sQxBhfJE-4FyLvW_JwXx2EwNA26tqIKmRIEu3ZBIQFlHJHURVigaogVryHsYkGcgTNKJ6BkgFMRM2dYCF5vmYtj-QKY5_p9d3fx2D-t_dv83dzzz8VHn3e5fmckcICdQ58tDfn9bRKb-5IOd_78v4v09F_rk2_eTVn_pcvr7B-uft87_XU-9_feAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQagCzDQqIA-yJCQi0HCKBACIKwgIoEAAAAJA0QEAJAwKdgYBLrCRACBFAAMEAIAAUZAAgAAEgAQiACQAoEAAEAgEAAAAAAgEADAwADgAtBAIAAQHQMUwoAFAsIEjMiIUwIQoEggJbKBBICgQVwgCLHAigERMFAAgCQAVgAAAsVgMQSAlYkECWEG0AABAAgFFKFQik6MAQwJmy1U4om0ZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAACAA.f_wACHwAAAAA; _cc_id=a5350f40adf077346e2ddfbc3945f34f; panoramaId_expiry=1703695755003; panoramaId=f2dca077afece39eea354494d2fe185ca02c4c5af4b316b5a480cc2049bb8161; panoramaIdType=panoDevice; __gads=ID=2854876d02e39999:T=1703090954:RT=1703090954:S=ALNI_MZgvj694RiOqmUkEv98XpZE7hLPDA; __gpi=UID=00000d24162c7afb:T=1703090954:RT=1703090954:S=ALNI_Ma7vkJu1-ObIR40_IBIKhlc-2V0tg; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Dec+20+2023+18%3A52%3A55+GMT%2B0200+(Eastern+European+Standard+Time)&version=202311.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5787432d-8422-4227-a270-e88ceb3d760f&interactionCount=1&landingPath=NotLandingPage&groups=C0002%3A1%2CC0001%3A1%2CC0004%3A1%2CC0003%3A1%2CV2STACK42%3A1&geolocation=LT%3BVL&AwaitingReconsent=false; cto_bundle=i3SioV9HWUdtRVp0cDdaJTJGT3RSd0ZISFR4UjFqcmtFMGVDcnZOblNiMjNCZDBrUWUlMkJpR0FTVVE0a1BNOHlEcHBLJTJCY0pYR2NCOHpKRm1RRG5RUHJpVTRvSTlUc082Sk9mOGZpYjJnY2M4a09vJTJCeU9sc1d1a1JXOFp2YmFFeGxBODJjNldMejdVMldIZnhqRGZSUVBtREZzdzROdyUzRCUzRA; mp_942a098c72ecbdd6c0d9c00fe8308319_mixpanel=%7B%22distinct_id%22%3A%20%2218c882199e624a-034b25690e05f4-4c657b58-144000-18c882199e712fe%22%2C%22%24device_id%22%3A%20%2218c882199e624a-034b25690e05f4-4c657b58-144000-18c882199e712fe%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; FCNEC=%5B%5B%22AKsRol9L6lnJOoEbbQFDhaHHGz6Vu0FXO-vEoYOjcPOqqlzk-Yd3KCHEF1ciCRuxR0btr9dLGEtx9FzfrYftLlQJ0epAJ-f0hO_2p8KUZdyIzV0Ew7v-AZhbDCNzM_7toQ6euiCKs-kgiSFcv1juOhpsKKzQ5NK1VQ%3D%3D%22%5D%2Cnull%2C%5B%5B5%2C%22226%22%5D%5D%5D; _ga_38V2BZ2HMF=GS1.1.1703090952.1.1.1703091188.48.0.0',
#     'if-modified-since': 'Wed, 20 Dec 2023 16:52:55 GMT',
#     'referer': 'https://www.flightradar24.com/data/airports',
#     'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
# }
        
#         response = requests.get(fr_url, cookies=cookies, headers=headers,)
#         response.raise_for_status()
#         #print(response.status_code)
#         #print(response)
#         if response.status_code == 200:




# Code below is just an example for reference

# def get_city_data(cities_data):
#     for city_info in cities_data:
#         city_code = city_info.get('Airport Code')
#         if city_code:
#             city_data = {"City Code": city_code, "General Info": None, "Arrivals": None, "Departures": None}

#             try:
#                 # General Info
#                 general_url = f"https://www.flightradar24.com/data/airports/{city_code}"
#                 general_response = requests.get(general_url)
#                 general_response.raise_for_status()
#                 general_soup = BeautifulSoup(general_response.content, 'html.parser')
#                 city_data["General Info"] = general_soup  # Store general information, modify as needed

#                 # Arrivals
#                 arrivals_url = f"https://www.flightradar24.com/data/airports/{city_code}/arrivals"
#                 arrivals_response = requests.get(arrivals_url)
#                 arrivals_response.raise_for_status()
#                 arrivals_soup = BeautifulSoup(arrivals_response.content, 'html.parser')
#                 city_data["Arrivals"] = arrivals_soup  # Store arrivals information, modify as needed

#                 # Departures
#                 departures_url = f"https://www.flightradar24.com/data/airports/{city_code}/departures"
#                 departures_response = requests.get(departures_url)
#                 departures_response.raise_for_status()
#                 departures_soup = BeautifulSoup(departures_response.content, 'html.parser')
#                 city_data["Departures"] = departures_soup  # Store departures information, modify as needed

#             except Exception as e:
#                 print(f"An error occurred for {city_code}: {e}")

#             # Process or store city_data as needed
#             print(city_data)

# # Example usage with your provided dictionary
# city_info_list = [{'City': 'Dubai', 'Airport': 'Dubai International Airport', 'Airport Code': 'DXB', 'Passengers': '66,069,981'}, {'City': 'London', 'Airport': 'London Heathrow Airport', 'Airport Code': 'LHR', 'Passengers': '58,243,060'}, {'City': 'Amsterdam', 'Airport': 'Amsterdam Airport Schiphol', 'Airport Code': 'AMS', 'Passengers': '52,467,346'}, {'City': 'Paris', 'Airport': 'Paris-Charles de Gaulle Airport', 'Airport Code': 'CDG', 'Passengers': '51,763,569'}, {'City': 'Istanbul', 'Airport': 'Istanbul Airport', 'Airport Code': 'IST', 'Passengers': '48,521,725'}, {'City': 'Frankfurt', 'Airport': 'Frankfurt Airport', 'Airport Code': 'FRA', 'Passengers': '44,771,711'}, {'City': 'Madrid', 'Airport': 'Madrid-Barajas Airport', 'Airport Code': 'MAD', 'Passengers': '36,231,191'}, {'City': 'Doha', 'Airport': 'Hamad International Airport', 'Airport Code': 'DOH', 'Passengers': '35,726,721'}, {'City': 'Singapore', 'Airport': 'Singapore Changi Airport', 'Airport Code': 'SIN', 'Passengers': '31,902,000'}, {'City': 'London', 'Airport': 'London Gatwick Airport', 'Airport Code': 'LGW', 'Passengers': '30,145,083'}]

# get_city_data(city_info_list)


#crawl(time_limit=60, source='lrytas', return_format='csv')