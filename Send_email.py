from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time

# Gmail credentials
SENDER_EMAIL = "k2485611@gmail.com"  # Replace with your email
SENDER_PASSWORD = "siva@667"  # Replace with your password
RECIPIENT_EMAIL = "sivasurya.mtrs@gmail.com"  # Replace with the recipient's email

try:
    # ChromeDriver setup with options
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)

    # Step 1: Open the Gmail login URL
    driver.get(
        "https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail"
    )

    # Step 2: Enter email and click "Next"
    email_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "identifierId"))
    )
    email_field.send_keys(SENDER_EMAIL)

    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "identifierNext"))
    )
    next_button.click()

    # Step 3: Enter password and click "Next"
    password_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "password"))  # Updated field name
    )
    password_field.send_keys(SENDER_PASSWORD)

    password_next = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "passwordNext"))
    )
    password_next.click()

    # Step 4: Wait until the inbox loads
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[text()='Compose']"))
    )
    print("Successfully logged into Gmail!")

    # Step 5: Click the "Compose" button
    compose_button = driver.find_element(By.XPATH, "//div[text()='Compose']")
    compose_button.click()

    # Step 6: Fill in the email
    to_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "to"))
    )
    to_field.send_keys(RECIPIENT_EMAIL)

    subject_field = driver.find_element(By.NAME, "subjectbox")
    subject_field.send_keys("DEMO")

    message_body = driver.find_element(By.XPATH, "//div[@role='textbox']")
    message_body.send_keys("This is the demo mail.")

    # Step 7: Click the "Send" button
    send_button = driver.find_element(By.XPATH, "//div[text()='Send']")
    send_button.click()
    print("Email sent successfully!")

    # Step 8: Verify email under sent items
    # Click "Sent" on the left menu
    sent_items_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'sent')]"))
    )
    sent_items_button.click()

    # Wait for the "Sent Items" to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//span[contains(text(), '{RECIPIENT_EMAIL}')]")
        )
    )
    print("Sent email verified successfully!")

except TimeoutException:
    print("An element took too long to load, possibly blocked by CAPTCHA or network issues.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()  # Ensure the browser closes
