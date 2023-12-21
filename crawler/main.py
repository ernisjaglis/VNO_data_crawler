
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

import requests
import csv
import os
#import time



# Defining function to get a list of busiest airports by passenger traffic in 2022 from wiki
wiki_url = "https://en.wikipedia.org/wiki/List_of_busiest_airports_by_passenger_traffic"
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
        print(response)
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
                        airport_name = cells[1].text.strip()
                        location = cells[2].text.strip()
                        country = cells[3].text.strip()
                        airport_code = cells[4].text.strip()
                        passengers = cells[5].text.strip()
                        airport_code_split = airport_code.split('/')[0]
                        busiest_airports_result.append({
                            'Airport Name': airport_name,
                            'Location': location,
                            'Country': country, 
                            'Airport Code': airport_code_split,
                            'Passengers': passengers})
                        #print(f"Airport Name: {airport_name}, Location: {location}, Country: {country}, Airport Code: {airport_code_split}, Passengers: {passengers}")
            else:
                print("Table not found on the page.")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


get_busiest_airports()
#print(busiest_airports_result)
#print(type(busiest_airports_result))



# Defining save to csv function to save dictionary of busiest airports data gathered with 'get_busiest_airports' function
#sample_data_folder = 'sample data'
#file_name = 'busiest_airports_result.csv'

def save_to_csv(data, folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


# Save the data to a CSV file in the 'sample data' folder
#save_to_csv(busiest_airports_result, sample_data_folder, file_name)



# # in this part extracting airport codes from list of dictionaries and creating list with only airport codes
all_airports_codes = [airport.get('Airport Code') for airport in busiest_airports_result]
print(all_airports_codes)
# #print(type(all_airports_codes))


# Function example to create url's for further data gathering according the list created with 'get_busiest_airports' function
all_airports_urls = {}

def url_by_airport_code(airport_code):
    all_airports_url = []
    for airport_code in all_airports_codes:
        try:
            general_url = f"https://www.flightradar24.com/data/airports/{airport_code}"
            arrivals_url = f"https://www.flightradar24.com/data/airports/{airport_code}/arrivals"
            departures_url = f"https://www.flightradar24.com/data/airports/{airport_code}/departures"
            all_airports_urls[airport_code] = {
            'general_url': general_url,
            'arrivals_url': arrivals_url,
            'departures_url': departures_url}

        except Exception as e:
            print(f"An error occurred for {airport_code}: {e}")


# Call the function with each airport code
for airport_code in all_airports_codes:
    url_by_airport_code(airport_code)

print(all_airports_urls) #might be commented, left uncommented for debugging purposes



# Defining function to get data (some texts, some statistics/numbers, photos) of airports from flightradar website

def get_airports_general_data():
    try:
        cookies = {
    '_ga': 'GA1.1.955066919.1702577494',
    'OptanonAlertBoxClosed': '2023-12-14T18:11:35.505Z',
    'eupubconsent-v2': 'CP2xZ3AP2xZ3AAcABBENAeEsAP_gAEPgAAYgg1NX_H__bW9r8Xr3aft0eY1P99j77sQxBhfJE-4FyLvW_JwXx2EwNA26tqIKmRIEu3ZBIQFlHJHURVigaogVryHsYkGcgTNKJ6BkgFMRI2dYCF5vmYtj-QKY5_p9d3fx2D-t_dv83dzzz8VHn3e5fmckcKCdQ58tDfn9bRKb-5IOd_78v4v09F_rk2_eTVn_pcvr7B-uft87_XU-9_fAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQagCzDQqIA-yJCQi0HCKBACIKwgIoEAAAAJA0QEAJAwKdgYBLrCRACBFAAMEAIAAUZAAgAAEgAQiACQAoEAAEAgEAAAAAAgEADAwADgAtBAIAAQHQMUwoAFAsIEjMiIUwIQoEggJbKBBICgQVwgCLDAigERMFAAgCQAVgAAAsVgMQSAlYkECWEG0AABAAgFFKFQik6MAQwJmy1U4om0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAACAA.f_wACHwAAAAA',
    '_cc_id': 'fb0816012b5d76752c8bfb69fb358d08',
    '_pbjs_userid_consent_data': '3524755945110770',
    '_lr_env_src_ats': 'false',
    'showAds': 'no',
    'cf_clearance': 'A_eaUigtk_sFoSQ7cKivNHbKqCH8WI21QNUzQ5Y0kDs-1702920799-0-1-f20b3d2d.5e239843.8364013c-150.0.0',
    'pbjs-unifiedid': '%7B%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222023-12-20T16%3A37%3A03%22%7D',
    'pbjs-unifiedid_last': 'Wed%2C%2020%20Dec%202023%2016%3A37%3A01%20GMT',
    '__cfruid': '33ab707af61fda7c339d0647db42d44674cd3ae9-1703174523',
    '_ga_38V2BZ2HMF': 'deleted',
    '__gads': 'ID=8c2adcf9dc54e8ce:T=1702577495:RT=1703184551:S=ALNI_MYyXSJraUiHDJ8cv0VwT8Hp5VrcfQ',
    '__gpi': 'UID=00000d1a250ff150:T=1702577495:RT=1703184551:S=ALNI_MY3HUAswN6XQTfPUmgflzZ31jT3fg',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Thu+Dec+21+2023+20%3A49%3A25+GMT%2B0200+(Eastern+European+Standard+Time)&version=202311.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=75287ff9-21a8-43d3-8f5d-9f69584b9897&interactionCount=1&landingPath=NotLandingPage&groups=C0002%3A1%2CC0001%3A1%2CC0004%3A1%2CC0003%3A1%2CV2STACK42%3A1&geolocation=LT%3BVL&AwaitingReconsent=false',
    'mp_942a098c72ecbdd6c0d9c00fe8308319_mixpanel': '%7B%22distinct_id%22%3A%20%2218c6986db50392-094b3f2d364218-26001951-144000-18c6986db51b9a%22%2C%22%24device_id%22%3A%20%2218c6986db50392-094b3f2d364218-26001951-144000-18c6986db51b9a%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%7D',
    '_ga_38V2BZ2HMF': 'GS1.1.1703184549.23.0.1703184566.43.0.0',
    'FCNEC': '%5B%5B%22AKsRol-rUVF9E2TfajG1vgttRuI3WUuj897z33GNUbrBqvkic9_-J8hDYBwKgP5WaOUV0HQLXnpJrT6ds58TM_AF_Jcng8mH-Se6KOLCga3bik78dhwz6s3cUhM2nhPIZ88KCioc0PJSS55Xz29caW47DGY9L7yRSw%3D%3D%22%5D%2Cnull%2C%5B%5B5%2C%22518%22%5D%5D%5D',
    'cto_bundle': 'l24q8l80R2VyaDdIJTJGeWJxNlF5dGFJNzBIVmpFUnlEdXJMT2liYzZTblNNTzlnTSUyRjRNbGFGNmM0cGhiend4WHN2V3Z1VnVDU1olMkZGR2lZeTN6b20yaCUyQm16NVd6SEc4M2NqSEtwdTBZaG9NJTJCWWNuZE5HTkElMkJiZG9tSXlncWZxZHkzMWdkd1lhWnBMMyUyRnczUjlvRzFkQ1BrRjZQb0l5d2Y0dzZBOTQzMlpDamp0b3BtUSUzRA',
}
        headers = {
    'authority': 'www.flightradar24.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en,en-US;q=0.9,lt;q=0.8,ru;q=0.7,pl;q=0.6',
    'cache-control': 'max-age=0',
    # 'cookie': '_ga=GA1.1.955066919.1702577494; OptanonAlertBoxClosed=2023-12-14T18:11:35.505Z; eupubconsent-v2=CP2xZ3AP2xZ3AAcABBENAeEsAP_gAEPgAAYgg1NX_H__bW9r8Xr3aft0eY1P99j77sQxBhfJE-4FyLvW_JwXx2EwNA26tqIKmRIEu3ZBIQFlHJHURVigaogVryHsYkGcgTNKJ6BkgFMRI2dYCF5vmYtj-QKY5_p9d3fx2D-t_dv83dzzz8VHn3e5fmckcKCdQ58tDfn9bRKb-5IOd_78v4v09F_rk2_eTVn_pcvr7B-uft87_XU-9_fAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQagCzDQqIA-yJCQi0HCKBACIKwgIoEAAAAJA0QEAJAwKdgYBLrCRACBFAAMEAIAAUZAAgAAEgAQiACQAoEAAEAgEAAAAAAgEADAwADgAtBAIAAQHQMUwoAFAsIEjMiIUwIQoEggJbKBBICgQVwgCLDAigERMFAAgCQAVgAAAsVgMQSAlYkECWEG0AABAAgFFKFQik6MAQwJmy1U4om0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAACAA.f_wACHwAAAAA; _cc_id=fb0816012b5d76752c8bfb69fb358d08; _pbjs_userid_consent_data=3524755945110770; _lr_env_src_ats=false; showAds=no; cf_clearance=A_eaUigtk_sFoSQ7cKivNHbKqCH8WI21QNUzQ5Y0kDs-1702920799-0-1-f20b3d2d.5e239843.8364013c-150.0.0; pbjs-unifiedid=%7B%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222023-12-20T16%3A37%3A03%22%7D; pbjs-unifiedid_last=Wed%2C%2020%20Dec%202023%2016%3A37%3A01%20GMT; __cfruid=33ab707af61fda7c339d0647db42d44674cd3ae9-1703174523; _ga_38V2BZ2HMF=deleted; __gads=ID=8c2adcf9dc54e8ce:T=1702577495:RT=1703184551:S=ALNI_MYyXSJraUiHDJ8cv0VwT8Hp5VrcfQ; __gpi=UID=00000d1a250ff150:T=1702577495:RT=1703184551:S=ALNI_MY3HUAswN6XQTfPUmgflzZ31jT3fg; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Dec+21+2023+20%3A49%3A25+GMT%2B0200+(Eastern+European+Standard+Time)&version=202311.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=75287ff9-21a8-43d3-8f5d-9f69584b9897&interactionCount=1&landingPath=NotLandingPage&groups=C0002%3A1%2CC0001%3A1%2CC0004%3A1%2CC0003%3A1%2CV2STACK42%3A1&geolocation=LT%3BVL&AwaitingReconsent=false; mp_942a098c72ecbdd6c0d9c00fe8308319_mixpanel=%7B%22distinct_id%22%3A%20%2218c6986db50392-094b3f2d364218-26001951-144000-18c6986db51b9a%22%2C%22%24device_id%22%3A%20%2218c6986db50392-094b3f2d364218-26001951-144000-18c6986db51b9a%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%7D; _ga_38V2BZ2HMF=GS1.1.1703184549.23.0.1703184566.43.0.0; FCNEC=%5B%5B%22AKsRol-rUVF9E2TfajG1vgttRuI3WUuj897z33GNUbrBqvkic9_-J8hDYBwKgP5WaOUV0HQLXnpJrT6ds58TM_AF_Jcng8mH-Se6KOLCga3bik78dhwz6s3cUhM2nhPIZ88KCioc0PJSS55Xz29caW47DGY9L7yRSw%3D%3D%22%5D%2Cnull%2C%5B%5B5%2C%22518%22%5D%5D%5D; cto_bundle=l24q8l80R2VyaDdIJTJGeWJxNlF5dGFJNzBIVmpFUnlEdXJMT2liYzZTblNNTzlnTSUyRjRNbGFGNmM0cGhiend4WHN2V3Z1VnVDU1olMkZGR2lZeTN6b20yaCUyQm16NVd6SEc4M2NqSEtwdTBZaG9NJTJCWWNuZE5HTkElMkJiZG9tSXlncWZxZHkzMWdkd1lhWnBMMyUyRnczUjlvRzFkQ1BrRjZQb0l5d2Y0dzZBOTQzMlpDamp0b3BtUSUzRA',
    'if-modified-since': 'Thu, 21 Dec 2023 18:49:24 GMT',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

        
        response = requests.get(fr_url, cookies=cookies, headers=headers,)
        response.raise_for_status()
        #print(response.status_code)
        #print(response)
        if response.status_code == 200:




#crawl(time_limit=60, source='lrytas', return_format='csv')