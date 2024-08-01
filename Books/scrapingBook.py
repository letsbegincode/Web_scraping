from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver with the Service object
chrome_options = Options()
chrome_options.add_argument("--disable-search-engine-choice-screen")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

try:
    # Open the URL
    driver.get("https://www.bookswagon.com/promo-best-seller/best-seller/03AC998EBDC2")

    # Function to perform slow scrolling and click the "Load more" button if found
    def slow_scroll_and_click():
        # Scroll down in increments
        scroll_increment = 200  # Adjust this value as needed
        current_position = 0
        while True:
            # Scroll by the increment
            driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
            current_position += scroll_increment
            time.sleep(2)  # Adjust this value to control the scroll speed

            # Check if the "Load more" button is present and click it
            try:
                load_more_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#lastPostLoader .more-load-page"))
                )
                if load_more_button:
                    print("Found 'Load more' button. Clicking...")
                    load_more_button.click()
                    time.sleep(3)  # Wait for new content to load
                    continue  # Continue scrolling after loading more content
            except Exception as e:
                print("No 'Load more' button found or an error occurred:", e)
            
            # Check if we've reached the bottom of the page
            new_position = driver.execute_script("return window.scrollY + window.innerHeight;")
            document_height = driver.execute_script("return document.body.scrollHeight;")
            
            if new_position >= document_height:
                print("Reached the end of the page.")
                break

    # Perform slow scrolling with "Load more" button handling
    slow_scroll_and_click()

    # Get the final HTML content of the page
    html_content = driver.page_source

    # Optionally, save the content to a file
    with open("file-output.txt", "w", encoding="utf-8") as file:
        file.write(html_content)

finally:
    # Ensure the driver is closed properly
    driver.quit()
