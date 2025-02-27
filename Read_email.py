from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException



class GmailPage:
    # The login page
    EMAIL_FIELD = (By.ID, "identifierId")
    NEXT_BUTTON_EMAIL = (By.ID, "identifierNext")
    PASSWORD_FIELD = (By.NAME, "password")
    NEXT_BUTTON_PASSWORD = (By.ID, "passwordNext")

    # The inbox page
    COMPOSE_BUTTON = (By.XPATH, "//div[text()='Compose']")
    FIRST_EMAIL = (By.XPATH, "//table//tr[@role='row']")
    EMAIL_BODY = (By.XPATH, "//div[@role='listitem']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open_login_page(self):
        self.driver.get(
            "https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com"
        )

    def enter_email(self, email):
        email_field = self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))
        email_field.send_keys(email)

    def click_next_email(self):
        next_button = self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON_EMAIL))
        next_button.click()

    def enter_password(self, password):
        password_field = self.wait.until(EC.presence_of_element_located(self.PASSWORD_FIELD))
        password_field.send_keys(password)

    def click_next_password(self):
        next_button = self.wait.until(
            EC.element_to_be_clickable(self.NEXT_BUTTON_PASSWORD))
        next_button.click()

    def wait_for_inbox(self):
        self.wait.until(EC.presence_of_element_located(self.COMPOSE_BUTTON))

    def open_first_email(self):
        first_email = self.wait.until(EC.presence_of_element_located(self.FIRST_EMAIL))
        first_email.click()

    def verify_email_content(self, required_content):
        email_body = self.wait.until(EC.presence_of_element_located(self.EMAIL_BODY))
        return required_content in email_body.text


# Test Script using Page Object Model

def test_gmail_content_verification():
    # Gmail credentials
    SENDER_EMAIL = "k2485611@gmail.com"  # Replace with your email
    SENDER_PASSWORD = "siva@667"  # Replace with your password
    REQUIRED_CONTENT = "Welcome"  # Content to be verified

    # Setup ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    try:

        gmail_page = GmailPage(driver)

        #  login
        gmail_page.open_login_page()
        gmail_page.enter_email(SENDER_EMAIL)
        gmail_page.click_next_email()
        gmail_page.enter_password(SENDER_PASSWORD)
        gmail_page.click_next_password()


        gmail_page.wait_for_inbox()
        print("Successfully logged into Gmail!")


        gmail_page.open_first_email()
        if gmail_page.verify_email_content(REQUIRED_CONTENT):
            print(f"Email content verified: '{REQUIRED_CONTENT}' found!")
        else:
            print(f"Email content not found: '{REQUIRED_CONTENT}' is missing.")

    except TimeoutException:
        print(
            "An element took too long to load, possibly blocked by CAPTCHA or network issues."
        )
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


# Call test
if __name__ == "__main__":
    test_gmail_content_verification()
