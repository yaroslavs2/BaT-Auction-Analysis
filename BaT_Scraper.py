from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(options=options)

# URL of the webpage
url = 'https://bringatrailer.com/mercedes-benz/190e-23-16/'

# Open the URL
driver.get(url)

# Initialize an empty list to store the results
auctions = []
processed_titles = set()  # Track titles to avoid re-adding

iteration = 0
while True:
    # Wait a bit for the content to load
    time.sleep(10)

    # Refresh the list of 'content-main' divs after each 'Show More' click
    content_main_divs = driver.find_elements(By.CLASS_NAME, 'content-main')
    print(f"Iteration {iteration}: Found {len(content_main_divs)} content-main divs")

    # Iterate through each div with class 'content-main'
    for div in content_main_divs:
        # Use WebDriverWait on individual auction elements to ensure they are fully loaded
        try:
            # Wait until the title and result elements are present within each div
            title_element = WebDriverWait(div, 10).until(
                EC.presence_of_element_located((By.XPATH, ".//h3[@data-bind='html: title']"))
            )
            title = title_element.text.strip()

            result_element = WebDriverWait(div, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'item-results'))
            )
            result = result_element.text.strip()
            
            excerpt_element = WebDriverWait(div, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "item-excerpt"))
            )
            auction_excerpt = excerpt_element.get_attribute('innerHTML').strip()
#             print(f"EXCERPT:", auction_excerpt)
            # Append the title and result to the list if it's not already processed
            if auction_excerpt not in processed_excerpts:
                auctions.append({'title': title, 'result': result})
                processed_excerpts.add(auction_excerpt)  # Mark this title as processed
                print(f"Added auction: {title} - {result}")

        except Exception as e:
            print(f"Error processing div: {e}")

    # Take a screenshot for debugging
    driver.save_screenshot(f'screenshot_iteration_{iteration}.png')

    # Try to find the 'Show More' button and click it
    try:
        show_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, './/span[@data-bind="hidden: itemsLoading"]'))
        )
        show_more_button.click()
        print("Clicked 'Show More' button")

        # Wait for new content to be added by monitoring number of 'content-main' divs
        WebDriverWait(driver, 10).until(
            lambda driver: len(driver.find_elements(By.CLASS_NAME, 'content-main')) > len(content_main_divs)
        )
    except Exception as e:
        # If 'Show More' button is not found or not clickable, break the loop
        driver.save_screenshot('error_screenshot.png')
        print(f"No more 'Show More' button or error: {e}")
        break

    iteration += 1

# Close the WebDriver
driver.quit()

print("Total auctions scraped:", len(auctions))

df = pd.DataFrame(auctions)

price_pattern = r"(?:Sold for USD|Bid to USD) \$(\d{1,3}(?:,\d{3})*)"
date_pattern = r"on (\d{1,2}/\d{1,2}/\d{2})"

# Extract sale price and date
df["sale_price"] = df["result"].str.extract(price_pattern)[0]
df["sale_date"] = df["result"].str.extract(date_pattern)[0]

# Convert the sale price to a numeric column and remove commas
df["sale_price"] = df["sale_price"].str.replace(",", "").astype(float)

# Convert the sale date to a datetime object
df["sale_date"] = pd.to_datetime(df["sale_date"], format="%m/%d/%y", errors="coerce")


