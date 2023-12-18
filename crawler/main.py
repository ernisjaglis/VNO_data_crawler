
from requests import get
from lxml.etree import HTML


# Defining function to find the url based on users selection
def get_airport_url():
    # Creating dictionary with links to airports info
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

    # Asking the user to type name of the city he is interested
    city_input = input("Please enter the city you are interested in (Vilnius, Doha, Frankfurt): ").capitalize()

    # Validating user input of city
    if city_input not in airports_select["City"]:
        print("Invalid city input. Please choose from Vilnius, Doha, or Frankfurt.")
        return None

    # Asking user type of information he needs
    info_type_input = input("Enter the type of information you are interested in (General, Arrival, Departure): ").capitalize()

    # Validating user input
    if info_type_input not in ["General", "Arrival", "Departure"]:
        print("Invalid information type input. Please choose from General, Arrival, or Departure.")
        return None

    # Getting the index of the selected city
    city_index = airports_select["City"].index(city_input)

    # Gettimg the URL based on user input
    if info_type_input == "General":
        return airports_select["General_info_url"][city_index]
    elif info_type_input == "Arrival":
        return airports_select["Arrival_url"][city_index]
    elif info_type_input == "Departure":
        return airports_select["Departure_url"][city_index]

# Assigning selected by user details to url and naming it selected_url    
selected_url = get_airport_url()
print(selected_url) #can be commented, showing just for myself to see if process working



# Defining function to get data from url which user selected
def get_airport_data(url: selected_url):
    #print(url)
    try:
        response = get(url)
        if 
        

        html_content = response.text
        return html_content
    except requests.RequestException as e:
        print(f"Error fetching data from the webpage: {e}")
        return None

html_data = get_airport_data(selected_url)
print(html_data) #can be commented, showing just for myself to see if process working


