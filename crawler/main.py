
from requests import get
from bs4 import BeautifulSoup


# Dictionary with links to airports info. Had idea to get all link in automated way. Maybe later will add that function
airports_select = {
        "City": ["Vilnius", "Doha", "Frankfurt"],
        "General_info_url": ["https://www.flightradar24.com/data/airports/vno",
                             "https://www.flightradar24.com/data/airports/doh",
                             "https://www.flightradar24.com/data/airports/fra"],
        "Arrival_url": ["https://www.flightradar24.com/data/airports/vno/arrivals",
                        "https://www.flightradar24.com/data/airports/doh/arrivals",
                        "https://www.flightradar24.com/data/airports/fra/arrivals"],
        "Departure_url": ["https://www.flightradar24.com/data/airports/vno/departures",
                          "https://www.flightradar24.com/data/airports/doh/departures",
                          "https://www.flightradar24.com/data/airports/fra/departures"]
        }


# Variables
General_info = []
Arrival_info = []
Departure_info = []


# Defining function to find the url based on users selection
def get_airport_url():
    city_input = input("Please enter the city you are interested in (Vilnius, Doha, Frankfurt): ").capitalize()

    # Validating user input of city
    if city_input not in airports_select["City"]:
        print("Invalid city input. Please choose from Vilnius, Doha, or Frankfurt.")
        return None

    info_type_input = input("Enter the type of information you are interested in (General, Arrival, Departure): ").capitalize()

    # Validating user input
    if info_type_input not in ["General", "Arrival", "Departure"]:
        print("Invalid information type input. Please choose from General, Arrival, or Departure.")
        return None

    # Getting the index of the selected city
    city_index = airports_select["City"].index(city_input)

    # Gettimg the URL based on user input by index
    if info_type_input == "General":
        return airports_select["General_info_url"][city_index]
    elif info_type_input == "Arrival":
        return airports_select["Arrival_url"][city_index]
    elif info_type_input == "Departure":
        return airports_select["Departure_url"][city_index]
    

# Getting url and naming it selected_url    
selected_url = get_airport_url()
print("Selected url is: " + selected_url) #can be commented, showing just for myself to see if process working



# Defining function to get webpage data from url which user selected
def get_airport_data(selected_url):
    try:
       response = get(selected_url)
       soup = BeautifulSoup(response.content, "html.parser") #trying to use BeautifulSoup library
       if selected_url == airports_select["General_info_url"]:
            # Logic for General information dathering
            general_details = soup.find("div", class_="row cnt-airport-details")
            print(general_details)
       else:
            print("General details element not found on the page.")
       if selected_url == airports_select["Arrival_url"]:
            # Logic for Arrival information
            arrival_details = soup.find("div", class_="row cnt-airport-details")
            print(arrival_details)
       else:
            print("Arrival details element not found on the page.")
       if selected_url == airports_select["Departure_url"]:
            # Logic for Departure information
            departure_details = soup.find("div", class_="row cnt-airport-details")
            print(departure_details)
       else:
            print("Departure details element not found on the page.")
    except Exception as e:
        print(f"Error: {e}")

# Call the function with the selected URL
get_airport_data(selected_url)
print(get_airport_data(selected_url))



