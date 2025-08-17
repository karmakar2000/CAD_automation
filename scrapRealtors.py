import time
import os
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchWindowException, TimeoutException, NoSuchElementException

fetched_cities = set()

def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument(r"user-data-dir=C:\Users\Delta\AppData\Local\Google\Chrome\User Data") # Replace with your Chrome user data directory
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def try_catch(function):
    try:
        return function()
    except Exception as e:
        print(f"Error: {e}")
        return None

def click_filter_button(driver):
    """Clicks the filter button on the webpage."""
    try:
        filter_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "mapSearchMoreBtn"))
        )
        filter_button.click()
        print("Clicked on Filters button.")
    except TimeoutException:
        print("Timeout while clicking the filter button.")
    except Exception as e:
        print(f"Error clicking filter button: {e}")

def select_transaction_type(driver, transaction_type):
    try:
        transaction_type = transaction_type.capitalize()  # Ensure transaction type is capitalized properly
        # Click the radio button based on the transaction type
        radio_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, f"//input[@id='rdoTransactionTypeRes_{TRANSACTION_TYPE_IDS[transaction_type]}']"))
        )
        radio_button.click()

        print(f"Selected transaction type: {transaction_type}")
        time.sleep(2)  # Add a short delay to allow the page to update
    except TimeoutException:
        print("Timeout while selecting transaction type.")
    except NoSuchElementException:
        print(f"Transaction type '{transaction_type}' not found on the webpage.")
    except Exception as e:
        print(f"Error selecting transaction type: {e}")

# Assuming TRANSACTION_TYPE_IDS is defined as a dictionary mapping transaction types to their respective IDs:
TRANSACTION_TYPE_IDS = {
    "For sale": 0,
    "For rent": 1,
    "Sold": 2,
}



def select_property_type(driver, property_type):
    """Selects the specified property type from the dropdown."""
    try:
        # Click on the property type dropdown
        property_type_dropdown = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "select2-ddlPropertyTypeRes-container"))
        )
        property_type_dropdown.click()

        # Select the desired option
        option_to_select = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[text()='{property_type}']"))
        )
        option_to_select.click()

        print(f"Selected property type: {property_type}")
        time.sleep(2)  # Add a short delay to allow the page to update
    except TimeoutException:
        print("Timeout while selecting property type.")
    except Exception as e:
        print(f"Error selecting property type: {e}")

def click_apply_button(driver):
    """Clicks the Apply button on the filter panel."""
    try:
        apply_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "mapMoreFiltersSearchBtn"))
        )
        apply_button.click()
        print("Clicked on Apply button.")
    except TimeoutException:
        print("Timeout while clicking the Apply button.")
    except Exception as e:
        print(f"Error clicking Apply button: {e}")

def fill_min_price(driver, min_price):
    try:
        min_price_dropdown = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "select2-ddlMinPrice-container"))
        )
        min_price_dropdown.click()

        option_to_select = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{min_price}')]"))
        )
        option_to_select.click()

        print(f"Filled minimum price: {min_price}")
        time.sleep(2)  # Add a short delay to allow the page to update
    except TimeoutException:
        print("Timeout while filling minimum price.")
    except Exception as e:
        print(f"Error filling minimum price: {e}")

def fill_min_rent(driver, min_rent):
    try:
        min_rent_dropdown = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "select2-ddlMinRent-container"))
        )
        min_rent_dropdown.click()

        option_to_select = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{min_rent}')]"))
        )
        option_to_select.click()

        print(f"Filled minimum rent: {min_rent}")
        time.sleep(2)  # Add a short delay to allow the page to update
    except TimeoutException:
        print("Timeout while filling minimum rent.")
    except Exception as e:
        print(f"Error filling minimum rent: {e}")



def fill_max_price(driver, max_price):
    try:
        # Click the max price dropdown to open the options
        max_price_dropdown = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "select2-ddlMaxPrice-container"))
        )
        max_price_dropdown.click()

        # Select the desired max price option from the list
        option_to_select = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[@class='select2-results__option' and text()='{max_price}']"))
        )
        option_to_select.click()

        print(f"Filled maximum price: {max_price}")
        time.sleep(2)  # Add a short delay to allow the page to update
    except TimeoutException:
        print("Timeout while filling maximum price.")
    except Exception as e:
        print(f"Error filling maximum price: {e}")

def fill_max_rent(driver, max_rent):
    try:
        max_rent_dropdown = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "select2-ddlMaxRent-container"))
        )
        max_rent_dropdown.click()

        option_to_select = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{max_rent}')]"))
        )
        option_to_select.click()

        print(f"Filled maximum rent: {max_rent}")
        time.sleep(2)  # Add a short delay to allow the page to update
    except TimeoutException:
        print("Timeout while filling maximum rent.")
    except Exception as e:
        print(f"Error filling maximum rent: {e}")


def fill_beds(driver, beds):
    try:
        beds_dropdown = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "select2-ddlBeds-container"))
        )
        beds_dropdown.click()

        option_to_select = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[text()='{beds}']"))
        )
        option_to_select.click()

        print(f"Selected number of bedrooms: {beds}")
        time.sleep(2)  # Add a short delay to allow the page to update
    except TimeoutException:
        print("Timeout while selecting number of bedrooms.")
    except Exception as e:
        print(f"Error selecting number of bedrooms: {e}")




def fill_baths(driver, baths):
    try:
        baths_dropdown = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "select2-ddlBaths-container"))
        )
        baths_dropdown.click()

        option_to_select = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[text()='{baths}']"))
        )
        option_to_select.click()

        print(f"Selected number of bathrooms: {baths}")
        time.sleep(2)  # Add a short delay to allow the page to update
    except TimeoutException:
        print("Timeout while selecting number of bathrooms.")
    except Exception as e:
        print(f"Error selecting number of bathrooms: {e}")


def fill_sold_in_last(driver, sold_in_last):
    try:
        sold_in_last_dropdown = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "select2-ddlSoldWithin-container"))
        )
        sold_in_last_dropdown.click()

        option_to_select = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[text()='{sold_in_last}']"))
        )
        option_to_select.click()

        print(f"Filled 'Sold in Last' period: {sold_in_last}")
        time.sleep(2)  # Add a short delay to allow the page to update
    except TimeoutException:
        print("Timeout while filling 'Sold in Last' period.")
    except Exception as e:
        print(f"Error filling 'Sold in Last' period: {e}")

def scrape_property_details(driver, property_url):
    """Scrapes the detailed information of a property."""
    driver.get(property_url)
    
    # Wait for the property details to load
    time.sleep(5)
    
    property_details = {}
    
    # Scrape additional details here, e.g., property description, features, etc.
    try:
        property_details["Property_type"] = try_catch(
            lambda: driver.find_element(By.CSS_SELECTOR, "#propertyDetailsSectionContentSubCon_PropertyType .propertyDetailsSectionContentValue").text.strip()
        )

        property_details["Building_type"] = try_catch(
            lambda: driver.find_element(By.CSS_SELECTOR, "#propertyDetailsSectionContentSubCon_BuildingType .propertyDetailsSectionContentValue").text.strip()
        )

        property_details["Community Name"] = try_catch(
            lambda: driver.find_element(By.CSS_SELECTOR, "#propertyDetailsSectionContentSubCon_CommunityName .propertyDetailsSectionContentValue").text.strip()
        )

        property_details["Title"] = try_catch(
            lambda: driver.find_element(By.CSS_SELECTOR, "#propertyDetailsSectionContentSubCon_Title .propertyDetailsSectionContentValue").text.strip()
        )

        property_details["Annual Property Taxes"] = try_catch(
            lambda: driver.find_element(By.CSS_SELECTOR, "#propertyDetailsSectionContentSubCon_AnnualPropertyTaxes .propertyDetailsSectionContentValue").text.strip()
        )
        
        property_details["Parking_type"] = try_catch(
            lambda: driver.find_element(By.CSS_SELECTOR, "#propertyDetailsSectionContentSubCon_ParkingType .propertyDetailsSectionContentValue").text.strip()
        )

        property_details["TimeOnRealtor"] = try_catch(
            lambda: driver.find_element(By.CSS_SELECTOR, "#propertyDetailsSectionContentSubCon_TimeOnRealtor .propertyDetailsSectionContentValue").text.strip()
        )

        # Scrape realtor details
        realtor_details = {}
        realtor_details["Name"] = try_catch(
            lambda: driver.find_element(By.CSS_SELECTOR, ".realtorCardName").text.strip()
        )

        realtor_details["Phone"] = try_catch(
            lambda: driver.find_element(By.CSS_SELECTOR, ".realtorCardPhone .TelephoneNumber").text.strip()
        )

        realtor_details["Website"] = try_catch(
            lambda: driver.find_element(By.CSS_SELECTOR, ".realtorCardWebsite").get_attribute("href")
        )

        realtor_details["Email_Link"] = try_catch(
            lambda: driver.find_element(By.CSS_SELECTOR, ".lnkEmailRealtor").get_attribute("href")
        )

        realtor_details["Book_Showing_Link"] = try_catch(
            lambda: driver.find_element(By.CSS_SELECTOR, ".lnkEmailRealtorWithBooking").get_attribute("href")
        )

        property_details["Realtor_Details"] = realtor_details

    except Exception as e:
        print(f"Error scraping property details: {e}")

    return property_details



def scrape_page(driver, results, city_name):
    try:
        while True:
            # Wait for the search list to load
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mapSidebarBodyCon")))

            # Parse the search list
            property_list_container = driver.find_element(By.CSS_SELECTOR, "#mapSidebarBodyCon")
            WebDriverWait(driver, 60).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".select2-container--disabled"))
            )
            properties = property_list_container.find_elements(By.CSS_SELECTOR, ".cardCon")
            print(f"Found {len(properties)} properties on this page")

            for child_element in properties:
                bedrooms = try_catch(
                    lambda: [el for el in child_element.find_elements(By.CSS_SELECTOR, ".smallListingCardIconCon") if
                             "Bedrooms" in el.get_attribute("innerHTML")][0].find_element(By.CSS_SELECTOR,
                                                                                          ".smallListingCardIconTopCon").text.strip())
                bathrooms = try_catch(
                    lambda: [el for el in child_element.find_elements(By.CSS_SELECTOR, ".smallListingCardIconCon") if
                             "Bathrooms" in el.get_attribute("innerHTML")][0].find_element(By.CSS_SELECTOR,
                                                                                           ".smallListingCardIconTopCon").text.strip())

                price_str = try_catch(lambda: child_element.find_element(By.CSS_SELECTOR, ".smallListingCardPrice").text)
                price = None
                if price_str:
                    price_str = price_str.replace("$", "").replace(",", "").replace("/Monthly", "").replace("/sqft",
                                                                                                            "").strip()
                    try:
                        price = float(price_str)
                    except ValueError:
                        print(f"Could not convert price to float: {price_str}")

                address = try_catch(
                    lambda: child_element.find_element(By.CSS_SELECTOR, ".smallListingCardAddress").text.strip())

                # Ensure the address contains the city name or 'North York'
                if address and (city_name.lower() in address.lower() or "north york" in address.lower() or "north york" in city_name.lower()):
                    # Scrape property details page
                    details_url = try_catch(
                        lambda: child_element.find_element(By.CSS_SELECTOR, ".listingDetailsLink").get_attribute("href")
                    )
                    if details_url:
                        property_details = scrape_property_details(driver, details_url)
                        driver.back()  # Navigate back to the main listing page
                        WebDriverWait(driver, 60).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "#mapSidebarBodyCon"))
                        )  # Ensure the main page has loaded again
                        
                        result = {
                            "bedrooms": bedrooms,
                            "bathrooms": bathrooms,
                            "price": price,
                            "address": address,
                            **property_details,  # Include additional property details
                        }

                        # Print each property for debugging
                        print(result)

                        results.append(result)
                else:
                    print(f"Skipping property as address does not contain {city_name} or 'North York': {address}")

            # Check if there is a next page
            next_button = try_catch(lambda: driver.find_element(By.CSS_SELECTOR, ".nextPageButtonSelector"))
            if next_button and next_button.is_enabled():
                next_button.click()
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#mapSidebarBodyCon"))
                )  # Wait for the next page to load
            else:
                break

    except TimeoutException:
        print("Timeout while waiting for page elements to load.")
    except NoSuchWindowException:
        print("Browser window closed unexpectedly.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def get_coordinates(city_name):
    try:
        url = f"https://nominatim.openstreetmap.org/search?city={city_name}&format=json&limit=1"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.example.com",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()
        print(f"API Response for {city_name}: {data}")  # Print the response data for debugging
        if len(data) > 0:
            city_data = data[0]
            return {
                "ZoomLevel": 12,
                "CenterLat": float(city_data["lat"]),
                "CenterLon": float(city_data["lon"]),
                "LatitudeMax": float(city_data["boundingbox"][1]),
                "LongitudeMax": float(city_data["boundingbox"][2]),
                "LatitudeMin": float(city_data["boundingbox"][0]),
                "LongitudeMin": float(city_data["boundingbox"][3])
            }
        else:
            print(f"Coordinates for '{city_name}' not found.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None

def get_unique_filename(base_name):
    counter = 1
    filename = f"{base_name}.csv"
    while os.path.exists(filename):
        filename = f"{base_name}_{counter}.csv"
        counter += 1
    return filename

def fill_property_details(driver, transaction_type, property_type, min_price, min_rent, max_price, max_rent, beds, baths, sold_in_last):
    try:
        if property_type == "Multi Family":
            # Filter by price only for Multi Family properties
            if transaction_type.lower() in "for sale":
                fill_min_price(driver, min_price)
                fill_max_price(driver, max_price)
            elif transaction_type.lower() == "for rent":
                fill_min_rent(driver, min_rent)
                fill_max_rent(driver, max_rent)
            elif transaction_type.lower() in "sold":
                fill_sold_in_last(driver, sold_in_last)
                fill_min_price(driver, min_price)
                fill_max_price(driver, max_price)
        else:
            if transaction_type.lower() == "sold":
                fill_sold_in_last(driver, sold_in_last)
                fill_min_price(driver, min_price)
                fill_max_price(driver, max_price)
                fill_beds(driver, beds)
                fill_baths(driver, baths)
            elif transaction_type.lower() == "for sale":
                fill_min_price(driver, min_price)
                fill_max_price(driver, max_price)
                fill_beds(driver, beds)
                fill_baths(driver, baths)
            elif transaction_type.lower() == "for rent":
                fill_min_rent(driver, min_rent)
                fill_max_rent(driver, max_rent)
                fill_beds(driver, beds)
                fill_baths(driver, baths)
            else:
                print(f"Transaction type '{transaction_type}' not recognized.")
        
        select_property_type(driver, property_type)
        click_apply_button(driver)
    except Exception as e:
        print(f"Error filling property details: {e}")

def main():
    city_name = input("Enter the city name: ")

    if city_name in fetched_cities:
        print(f"Data for {city_name} has already been fetched.")
        return

    transaction_type = input("Enter the transaction type (For sale/For rent/Sold): ")

    city_coordinates = get_coordinates(city_name)

    if not city_coordinates:
        print(f"City '{city_name}' not found.")
        return

    start_url = f"https://www.realtor.ca/map#ZoomLevel={city_coordinates['ZoomLevel']}&Center={city_coordinates['CenterLat']}%2C{city_coordinates['CenterLon']}&LatitudeMax={city_coordinates['LatitudeMax']}&LongitudeMax={city_coordinates['LongitudeMax']}&LatitudeMin={city_coordinates['LatitudeMin']}&LongitudeMin={city_coordinates['LongitudeMin']}&CurrentPage=1&Sort=6-D&PropertyTypeGroupID=1&PropertySearchTypeId=0&TransactionTypeId={TRANSACTION_TYPE_IDS[transaction_type]}&Currency=CAD"
    
    driver = init_driver()
    driver.get(start_url)
    results = []

    try:
        click_filter_button(driver)
        select_transaction_type(driver, transaction_type.capitalize())

        property_type = input("Enter Property Type: ")
        select_property_type(driver, property_type)

        # Initialize variables based on transaction type
        min_price = None
        max_price = None
        min_rent = None
        max_rent = None
        beds = None
        baths = None
        sold_in_last = None

        if property_type == "Multi Family":
            if transaction_type.lower() == "for sale":
                min_price = input("Enter Min Price: ")
                max_price = input("Enter Max Price: ")
            elif transaction_type.lower() == "for rent":
                min_rent = input("Enter Min Rent: ")
                max_rent = input("Enter Max Rent: ")
            elif transaction_type.lower() == "sold":
                sold_in_last = input("Enter Sold in Last (years): ")
                min_price = input("Enter Min Price: ")
                max_price = input("Enter Max Price: ")
        else:
            if transaction_type.lower() == "for sale":
                min_price = input("Enter Min Price: ")
                max_price = input("Enter Max Price: ")
                beds = input("Enter Beds: ")
                baths = input("Enter Baths: ")

            elif transaction_type.lower() == "for rent":
                min_rent = input("Enter Min Rent: ")
                max_rent = input("Enter Max Rent: ")
                beds = input("Enter Beds: ")
                baths = input("Enter Baths: ")

            elif transaction_type.lower() == "sold":
                sold_in_last = input("Enter Sold in Last (years): ")
                min_price = input("Enter Min Price: ")
                max_price = input("Enter Max Price: ")
                beds = input("Enter Beds: ")
                baths = input("Enter Baths: ")
                
            else:
                print(f"Transaction type '{transaction_type}' not recognized.")
        

        fill_property_details(driver, transaction_type, property_type, min_price, min_rent, max_price, max_rent, beds, baths, sold_in_last)

        while True:
            scrape_page(driver, results, city_name)

            try:
                next_links = driver.find_elements(By.CSS_SELECTOR, ".lnkNextResultsPage")
                if not next_links:
                    print("No more pages available.")
                    break

                next_link = next_links[0]

                actions = ActionChains(driver)
                actions.move_to_element(next_link).perform()
                driver.execute_script("arguments[0].click();", next_link)
                time.sleep(5)  # Wait for the page to load

            except TimeoutException:
                print("No more pages or timeout occurred.")
                break
            except NoSuchWindowException:
                print("Browser window closed unexpectedly.")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break

    finally:
        if results:
            df = pd.DataFrame(results)
            filename = get_unique_filename("properties")
            df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
            print(df)
        else:
            print("No data found.")

        driver.quit()

    fetched_cities.add(city_name)


if __name__ == "__main__":
    main()



"""
Code By Deep Karmakar
The script includes functions for:

Initializing the Selenium WebDriver.
Filling property details based on the transaction type.
Selecting property types and applying filters.
Scraping data from multiple pages.

"""