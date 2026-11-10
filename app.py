import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import time

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

def find_email_field(driver):
    selectors = [
        (By.CSS_SELECTOR, "input[type='email']"),
        (By.CSS_SELECTOR, "input[name='email']"),
        (By.CSS_SELECTOR, "input[id='email']"),
        (By.XPATH, "//input[contains(@placeholder, 'email')]"),
    ]
    
    for selector in selectors:
        try:
            return driver.find_element(*selector)
        except Exception:
            continue
    
    return None

def find_password_field(driver):
    selectors = [
        (By.CSS_SELECTOR, "input[type='password']"),
        (By.CSS_SELECTOR, "input[name='password']"),
        (By.CSS_SELECTOR, "input[id='password']"),
        (By.XPATH, "//input[contains(@placeholder, 'pass')]"),
    ]
    
    for selector in selectors:
        try:
            return driver.find_element(*selector)
        except Exception:
            continue
    
    return None

def find_name_field(driver):
    selectors = [
        (By.CSS_SELECTOR, "input[name='name']"),
        (By.CSS_SELECTOR, "input[id='name']"),
        (By.XPATH, "//input[contains(@placeholder, 'name')]"),
    ]
    
    for selector in selectors:
        try:
            return driver.find_element(*selector)
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
        
        email_field = find_email_field(driver)
        password_field = find_password_field(driver)
        name_field = find_name_field(driver)
        
        if not email_field or not password_field:
            print("Email or password field not found.")
            return False
        
        email_field.send_keys(f"{full_username}@tempmail.com")
        password_field.send_keys(generate_random_string(12))
        
        if name_field:
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
    account_count = config.get('count', 10)
    
    if not website_url or not username_prefix:
        print("Error: Missing website URL or name in config.json.")
        return
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        for i in range(account_count):
            if create_account(driver, website_url, username_prefix):
                print("Account created successfully.")
            else:
                print("Failed to create account.")
            
            time.sleep(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
