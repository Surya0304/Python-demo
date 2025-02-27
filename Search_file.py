from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


# Page Object Model for Gmail Actions
class GmailPage:
    # Locators for Gmail login and search
    EMAIL_FIELD = (By.ID, "identifierId")
    NEXT_BUTTON_EMAIL = (By.ID, "identifierNext")
    PASSWORD_FIELD = (By.NAME, "password")
    NEXT_BUTTON_PASSWORD = (By.ID, "passwordNext")
    SEARCH_BOX = (By.NAME, "q")
    FIRST_SEARCH_RESULT = (By.XPATH, "//div[@role='main']//tr")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open_login_page(self):
        self.driver.get(
            "https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail"
        )

    def enter_email(self, email):
        email_field = self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))
        email_field.send_keys(email)

    def click_next_email(self):
        next_button = self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON_EMAIL))
        next_button.click()

    def enter_password(self, password):
        password_field = self.wait.until(
            EC.presence_of_element_located(self.PASSWORD_FIELD)
        )
        password_field.send_keys(password)

    def click_next_password(self):
        next_button = self.wait.until(
            EC.element_to_be_clickable(self.NEXT_BUTTON_PASSWORD)
        )
        next_button.click()

    def wait_for_inbox(self):
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='Compose']"))
        )

    def search_email(self, keyword):
        search_box = self.wait.until(EC.presence_of_element_located(self.SEARCH_BOX))
        search_box.send_keys(keyword)
        search_box.submit()

    def verify_search_result(self):
        try:
            result = self.wait.until(
                EC.presence_of_element_located(self.FIRST_SEARCH_RESULT)
            )
            print("Search result found!")
            return True
        except TimeoutException:
            print("No search results found!")
            return False


# Test Script using POM for Gmail Search Functionality
def test_gmail_search_functionality():
    # Gmail credentials
    SENDER_EMAIL = "k2485611@gmail.com"  # Replace with your email
    SENDER_PASSWORD = "siva@667"  # Replace with your password
    SEARCH_KEYWORD = "Invoice"  # Replace with the keyword to search in Gmail

    # ChromeDriver setup
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Initialize Gmail page object
        gmail_page = GmailPage(driver)

        # Step 1: Perform login
        gmail_page.open_login_page()
        gmail_page.enter_email(SENDER_EMAIL)
        gmail_page.click_next_email()
        gmail_page.enter_password(SENDER_PASSWORD)
        gmail_page.click_next_password()

        # Step 2: Wait for inbox to load
        gmail_page.wait_for_inbox()
        print("Successfully logged into Gmail!")

        # Step 3: Search for an email using provided keyword
        gmail_page.search_email(SEARCH_KEYWORD)

        # Step 4: Verify search results
        if gmail_page.verify_search_result():
            print(f"Search for keyword '{SEARCH_KEYWORD}' succeeded.")
        else:
            print(f"Search for keyword '{SEARCH_KEYWORD}' returned no results.")

    except TimeoutException:
        print(
            "An element took too long to load, possibly blocked by CAPTCHA or network issues."
        )
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


# Run the test
if __name__ == "__main__":
    test_gmail_search_functionality()
