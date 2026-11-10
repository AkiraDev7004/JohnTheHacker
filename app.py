import json
import random
import string
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from requests import post, exceptions as req_exceptions

CONFIG_PATH = "config.json"

def generate_random_suffix(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_account(driver, website_url, username):
    try:
        driver.get(website_url)
        time.sleep(0.5)
        
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        submit_button = driver.find_element(By.ID, "signup-btn")
        
        email_input.send_keys(username + "@tempmail.com")
        password_input.send_keys("SecurePass123!")
        submit_button.click()
        
        time.sleep(2)
        
        success_elements = driver.find_elements(By.XPATH, "//div[contains(text(), 'Success') or contains(text(), 'Account created')]")
        if len(success_elements) > 0:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error creating account for {username}: {str(e)}")
        return False

def main():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    website_url = config["website"]
    base_name = config["name"]
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Removed binary_location to let Selenium auto-detect Chrome
    
    driver = webdriver.Chrome(options=chrome_options)
    
    accounts_created = 0
    
    for i in range(100):
        suffix = generate_random_suffix()
        username = base_name + suffix
        
        print(f"[{i+1}/100] Creating account: {username}")
        
        if create_account(driver, website_url, username):
            accounts_created += 1
            
    driver.quit()
    
    print(f"\n=== SUMMARY ===")
    print(f"Total attempts: 100")
    print(f"Successful accounts: {accounts_created}")

if __name__ == "__main__":
    main()
