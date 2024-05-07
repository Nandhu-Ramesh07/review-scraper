from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

option = webdriver.ChromeOptions()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option)

site_url="https://www.amazon.in/Apple-iPhone-15-128-GB/product-reviews/B0CHX6NQMD/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"

page=driver.get(site_url)

# Function to scrape comments and click the next page button
def scrape_and_click_next_page():
    # Find all review text elements using their unique data-hook attribute
    review_elements = driver.find_elements(By.CSS_SELECTOR,'[data-hook="review-body"]')

    # Create a list to store the review texts
    reviews = []

    # Iterate over each review element and append the review text to the list
    for review_element in review_elements:
        review_text = review_element.text.strip()
        reviews.append(review_text)

    # Click the next page button if available
    try:
        next_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.a-last a'))
        )
        next_page_button.click()
        return reviews, True
    except Exception as e:
        print("No more pages available.")
        return reviews, False

# Initial scraping
all_reviews, next_page_available = scrape_and_click_next_page()

# Loop to scrape and click next page until no more pages are available
while next_page_available:
    new_reviews, next_page_available = scrape_and_click_next_page()
    all_reviews.extend(new_reviews)

# Create a DataFrame from the list of reviews
reviews_df = pd.DataFrame({'reviews': all_reviews})

# Save the DataFrame to a CSV file
reviews_df.to_csv('amazon_reviews.csv', index=False)

# Close the WebDriver
driver.quit()