import time
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchWindowException, TimeoutException


def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument(
        r"user-data-dir=C:\Users\Deep\AppData\Local\Google\Chrome\User Data")  # Replace with your Chrome user data directory
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def try_catch(function):
    try:
        return function()
    except Exception as e:
        print(f"Error: {e}")
        return None


def scrape_page(driver, results):
    try:
        # Wait for the search list to load
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mapSidebarBodyCon")))

        # Parse the search list
        property_list_container = driver.find_element(By.CSS_SELECTOR, "#mapSidebarBodyCon")
        WebDriverWait(driver, 60).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".select2-container--disabled"))
        )
        properties = property_list_container.find_elements(By.CSS_SELECTOR, ".cardCon")
        print(f"Found {len(properties)} properties on this page")

        # Add the results to the list
        for child_element in properties:
            bedrooms = try_catch(
                lambda: [el for el in child_element.find_elements(By.CSS_SELECTOR, ".smallListingCardIconCon") if
                         "Bedrooms" in el.get_attribute("innerHTML")][0].find_element(By.CSS_SELECTOR,
                                                                                      ".smallListingCardIconTopCon").text.strip())
            bathrooms = try_catch(
                lambda: [el for el in child_element.find_elements(By.CSS_SELECTOR, ".smallListingCardIconCon") if
                         "Bathrooms" in el.get_attribute("innerHTML")][0].find_element(By.CSS_SELECTOR,
                                                                                       ".smallListingCardIconTopCon").text.strip())

            price = try_catch(lambda: float(
                child_element.find_element(By.CSS_SELECTOR, ".smallListingCardPrice").text.replace("$", "").replace(",",
                                                                                                                    "").replace(
                    "/Monthly", "").strip()))
            address = try_catch(
                lambda: child_element.find_element(By.CSS_SELECTOR, ".smallListingCardAddress").text.strip())

            result = {
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "price": price,
                "address": address,
            }

            # Print each property for debugging
            print(result)

            results.append(result)
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


def main():
    city_name = input("Enter the city name: ")
    city_coordinates = get_coordinates(city_name)

    if not city_coordinates:
        print(f"City '{city_name}' not found.")
        return

    start_url = f"https://www.realtor.ca/map#ZoomLevel={city_coordinates['ZoomLevel']}&Center={city_coordinates['CenterLat']}%2C{city_coordinates['CenterLon']}&LatitudeMax={city_coordinates['LatitudeMax']}&LongitudeMax={city_coordinates['LongitudeMax']}&LatitudeMin={city_coordinates['LatitudeMin']}&LongitudeMin={city_coordinates['LongitudeMin']}&CurrentPage=1&Sort=6-D&PropertyTypeGroupID=1&PropertySearchTypeId=0&TransactionTypeId=3&Currency=CAD"
    driver = init_driver()
    driver.get(start_url)
    results = []

    try:
        while True:
            scrape_page(driver, results)

            try:
                # Check if there is a link to the next page
                next_links = driver.find_elements(By.CSS_SELECTOR, ".lnkNextResultsPage")
                if not next_links:
                    print("No more pages available.")
                    break

                next_link = next_links[0]

                # Scroll the element into view
                actions = ActionChains(driver)
                actions.move_to_element(next_link).perform()
                # Click on the next page link
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
        df = pd.DataFrame(results)
        df.to_csv("properties2.csv", index=False)
        print(df)

        # Close the web driver
        driver.quit()


if __name__ == "__main__":
    main()
