from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
import json
import sys
import requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import time
import sched
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()


class ApplicationNotificationBot:

    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.time_interval = 5
        self.flag = 1
        self.previous_data = ""
        self.scheduler.enter(self.time_interval, 1, self.run_function, (self.scheduler,))
        self.scheduler.run()

    def check_sentiment(self, query):
        scores = sia.polarity_scores(query)
        print(scores)
        key_with_highest_value = max(scores, key=scores.get)
        print(key_with_highest_value)
        sentiment_dict = {'neg': "#FF0000", 'pos': "#00FF00", 'neu': "#000000"}
        return_color = sentiment_dict[key_with_highest_value]
        return return_color

    def send_notification(self, message):
        url = "$slack_tocken"

        sentiment_color = self.check_sentiment(message)

        # All slack data
        slack_data = {

            "username": "UIC Bot",
            "attachments": [
                {
                    "color": sentiment_color,
                    "fields": [
                        {
                            "title": f"Application Status Bot :satellite:",
                            "value": message,
                            "short": "false",

                        }
                    ]
                }
            ]
        }

        # Size of the slack data
        byte_length = str(sys.getsizeof(slack_data))
        headers = {'Content-Type': "application/json",
                   'Content-Length': byte_length}

        # Posting requests after dumping the slack data
        response = requests.post(url, data=json.dumps(slack_data), headers=headers)

        # Post request is valid or not!
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

    def run_function(self, sc):
        self.main()  # Call the function to be executed
        self.scheduler.enter(self.time_interval, 1, self.run_function, (sc,))  # Schedule the function to run again
        # after the time interval

    def main(self):
        # Replace these with the appropriate values for your website
        url = '$uni_login_portal'
        username = '$username'
        password = '$password'

        # Configure Selenium webdriver with the path to your Chrome driver executable
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # Replace with your Chrome driver path
        chrome_driver_path = r"C:\Users\$chrome-drive-path"
        driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)

        # Navigate to the login page
        driver.get(url)

        # Find the username and password input fields and enter the values

        # Replace with the ID or other selector for the username input field
        username_input = driver.find_element('id',
                                             'email')
        username_input.send_keys(username)
        # Replace with the ID or other selector for the password input field
        password_input = driver.find_element('id',
                                             'password')
        password_input.send_keys(password)

        # Find the login button and click on it
        # Replace with the ID or other selector for the login button
        login_button = driver.find_element_by_tag_name('button')
        login_button.click()

        # Wait for the page to load after login (you can adjust the wait time as needed)
        wait = WebDriverWait(driver, 10)
        # Replace with the URL that indicates the successful login
        wait.until(
            EC.url_to_be('$succes_page'))

        # Now that you are logged in, you can scrape the webpage
        # For example, you can find elements by their IDs, classes, or other selectors,
        # and extract the desired information
        # using the element's text, attributes, etc.
        data_element = driver.find_element('id',
                                           'part_08ab941b-59b0-4c75-996f-fb9991cc60a5')
        # Replace with the ID or other selector for the data element

        data = data_element.text  # Extract the text content of the element

        # Do whatever you need with the scraped data
        print(data)
        if self.flag == 1:
            self.previous_data = ""

        if self.flag == 1:
            previous_data = data
            self.flag += 1
        else:
            if data != self.previous_data:
                self.send_notification(data)
            else:
                pass
        # Close the browser window
        driver.quit()


bot_obj = ApplicationNotificationBot()
bot_obj.main()
