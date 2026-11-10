import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def find_signup_button(driver):
    wait = WebDriverWait(driver, 15)
    
    selectors = [
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.CSS_SELECTOR, "input[type='submit']"),
        (By.XPATH, "//button[contains(text(), 'Sign')]"),
        (By.XPATH, "//button[contains(@class, 'signup')]"),
        (By.XPATH, "//a[contains(@href, '/register')]"),
    ]
    
    for selector in selectors:
        try:
            element = wait.until(EC.element_to_be_clickable(selector))
            return element
        except Exception:
            continue
    
    return None

def click_all_buttons(driver):
    buttons = driver.find_elements(By.CSS_SELECTOR, "button, [onclick], input[type='submit']")
    for button in buttons:
        try:
            button.click()
        except Exception:
            pass

def fill_date_fields(driver):
    date_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='date'], input[placeholder*='date']")
    for input_elem in date_inputs:
        try:
            input_elem.send_keys("09.09.1999")
        except Exception:
            pass

def handle_alerts(driver):
    try:
        driver.switch_to.alert.accept()
    except Exception:
        pass

def create_account(driver, website_url, username_prefix):
    driver.get(website_url)
    
    signup_button = find_signup_button(driver)
    if not signup_button:
        print("Signup button not found.")
        return False
    
    try:
        random_suffix = generate_random_string(8)
        full_username = f"{username_prefix}{random_suffix}"
        
        email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        name_field = driver.find_element(By.CSS_SELECTOR, "input[name='name'], input[id='name']")
        
        email_field.send_keys(f"{full_username}@tempmail.com")
        password_field.send_keys(generate_random_string(12))
        name_field.send_keys(full_username)
        
        signup_button.click()
        
        wait = WebDriverWait(driver, 5)
        handle_alerts(driver)
        fill_date_fields(driver)
        click_all_buttons(driver)
        
        return True
    except Exception:
        return False

def main():
    config_file = "config.json"
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found.")
        return
    
    website_url = config.get('website', '')
    username_prefix = config.get('name', '')
    
    if not website_url or not username_prefix:
        print("Error: Missing website URL or name in config.json.")
        return
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        for _ in range(10):
            if create_account(driver, website_url, username_prefix):
                print("Account created successfully.")
            else:
                print("Failed to create account.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
