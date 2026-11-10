#!/usr/bin/env python3
import json
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def load_config(path='config.json'):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print('Config file not found.')
        sys.exit(1)

def create_account(driver):
    driver.get(config['website'])
    def find_signup_button():
        selectors = [By.ID, By.NAME, By.XPATH]
        ids = ['signup-btn', 'sign-up', 'register', 'create-account']
        names = ['signup', 'sign_up', 'register', 'create_account']
        for sel_type in selectors:
            for val in ids + names:
                try:
                    return driver.find_element(sel_type, val)
                except Exception:
                    continue
        xpath_patterns = [
            '//button[contains(text(), "Sign Up")]',
            '//button[contains(text(), "Register")]',
            '//input[@type="submit"]',
            '//a[contains(@href, "/signup")]'
        ]
        for pat in xpath_patterns:
            try:
                return driver.find_element(By.XPATH, pat)
            except Exception:
                continue
        return None

    signup_btn = find_signup_button()
    if not signup_btn:
        print('Signup button not found.')
        sys.exit(1)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(signup_btn))
    driver.execute_script('arguments[0].click();', signup_btn)

    inputs = driver.find_elements(By.CSS_SELECTOR, 'input:not([disabled])')
    password_fields = [i for i in inputs if 'password' in (i.get_attribute('name') or '').lower() or 'pass' in (i.get_attribute('id') or '').lower()]
    email_fields = [i for i in inputs if 'email' in (i.get_attribute('name') or '').lower() or '@' in (i.get_attribute('placeholder') or '').lower()]
    username_field = None
    for inp in inputs:
        name = (inp.get_attribute('name') or '').lower()
        id_val = (inp.get_attribute('id') or '').lower()
        if 'user' in name or 'username' in name or 'login' in id_val or 'account' in id_val:
            username_field = inp
            break

    password = generate_random_string(14)
    for pf in password_fields:
        pf.clear()
        pf.send_keys(password)
    if len(password_fields) > 1 and not any(pf.get_attribute('value') == password for pf in password_fields):
        print('Password mismatch detected.')

    if email_fields:
        email = f"{config['name'].lower()}@{generate_random_string(6)}.com"
        ef = email_fields[0]
        ef.clear()
        ef.send_keys(email)

    if username_field:
        suffix_len = random.randint(4, 8)
        suffix = generate_random_string(suffix_len)
        new_username = f"{config['name']}{suffix}"
        username_field.clear()
        username_field.send_keys(new_username)

    submit_btn = find_signup_button()
    if submit_btn:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_btn))
        driver.execute_script('arguments[0].click();', submit_btn)

def main():
    global config
    config = load_config()
    count = config.get('count', 100)
    for i in range(count):
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        try:
            driver = webdriver.Chrome(options=options)
            create_account(driver)
        except Exception as e:
            print(f'Account {i+1} failed: {e}')
        finally:
            driver.quit()

if __name__ == '__main__':
    main()
