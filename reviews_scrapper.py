from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv


def locating_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    # Wait until element is visible
    WebDriverWait(driver, 20).until(EC.visibility_of(element))

# driver setup
options = webdriver.ChromeOptions()
# Start browser maximized
options.add_argument('start-maximized')  
driver = webdriver.Chrome(options=options)
link = input('Enter the Google Maps link: ')
number_of_reviews = int(input('Enter the number of reviews you want: '))
driver.get(link)

wait = WebDriverWait(driver, 20)
action = ActionChains(driver)

# Expanding reviews
try:
    more_comments = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'M77dve')))
    for comment in more_comments:
        text = comment.get_attribute('textContent')
        if 'التعليقات' in text or 'reviews' in text:
            locating_element(driver, comment)
            comment.click()
            break
except Exception as e:
    print("Error expanding reviews:", e)

wait.until(lambda driver: len(driver.find_elements(By.CLASS_NAME, 'RfnDt')) >= number_of_reviews)

# Collect review data
with open('reviews.csv', 'w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Name', 'Review', 'Comment', 'Number of Reviews', 'Review Date', 'Likes Number'])
    reviews = driver.find_elements(By.CLASS_NAME, 'jftiEf')

    for element in reviews[:number_of_reviews]:
        try:
            name = element.find_element(By.CLASS_NAME, 'd4r55').text.strip()
            comment = element.find_element(By.CLASS_NAME, 'wiI7pd').text.replace('\n', ' ')
            review = element.find_element(By.CLASS_NAME, 'kvMYJc').get_attribute('aria-label').strip()
            n_reviews_elements = element.find_elements(By.CLASS_NAME, 'RfnDt')
            n_reviews = ' · '.join([e.text.strip() for e in n_reviews_elements if e.text.strip()])
            post_date = element.find_element(By.CLASS_NAME, 'rsqaWe').text.strip()
            likes = element.find_element(By.CLASS_NAME, 'GBkF3d').text.replace('Like', '').strip()
            csv_writer.writerow([name, review, comment, n_reviews, post_date, likes])
        except Exception as e:
            print("Error processing a review:", e)

driver.quit()
