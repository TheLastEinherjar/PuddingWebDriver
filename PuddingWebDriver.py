from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
import time
import random

#Writen by Pudding and Everlong

class PuddingWebDriver:
    class TabNotFoundError(Exception):
        pass

    def __init__(self, driver:webdriver):
        self.driver = driver

    def wait_for_title(self, title, timeout=40):
        try:
            WebDriverWait(self.driver, timeout).until(lambda x: title in x.title)
            return True
        except (TimeoutException):
            return False

    def click_element(self, identifier, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(identifier))
            element.click()
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def refresh_page(self, timeout=40):
        try:
            self.driver.refresh()
            return True
        except (TimeoutException):
            return False

    def send_keys(self, identifier, keys, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(identifier))
            element.send_keys(keys)
            return True
        except (NoSuchElementException, TimeoutException):
            return False
        
    def type_keys(self, identifier, keys, min_time_to_key=0.1, max_time_to_key=0.2, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(identifier))
            for key in keys :
                element.send_keys(key)
                if key == ' ' :
                    self.sleep_range(min_time_to_key*3, max_time_to_key*3)
                else :
                    self.sleep_range(min_time_to_key, max_time_to_key)
                    
            return True
        except (NoSuchElementException, TimeoutException):
            return False
        
    def clear_element(self, identifier, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(identifier))
            element.clear()
            return True
        except (NoSuchElementException, TimeoutException):
            return False
        
    def get_attribute(self, element_identifier, attribute:str) :
        try :
            attribute_data = self.driver.find_element(element_identifier[0], element_identifier[1]).get_attribute(attribute)
            return attribute_data
        except : 
            return False
    
    def back(self):
        self.driver.back()

    def forward(self):
        self.driver.forward()

    def maximize(self) :
        self.driver.maximize_window()

    def switch_tab(self, tab_index):
        if tab_index < len(self.driver.window_handles):
            self.driver.switch_to.window(self.driver.window_handles[tab_index])
        else:
            raise self.TabNotFoundError("Tab not found in window_handles")

    def set_page_load_timeout(self, timeout):
        self.driver.set_page_load_timeout(timeout)

    def handle_alert(self, accept=True):
        try:
            if accept:
                alert = self.driver.switch_to.alert
                alert.accept()
            else:
                alert = self.driver.switch_to.alert
                alert.dismiss()
        except:
            print("Unexpected alert encountered")

    def sleep(self, seconds):
        time.sleep(seconds)

    def sleep_range(self, min_seconds, max_seconds):
        time.sleep(random.uniform(min_seconds, max_seconds))

    def get(self, url) :
        try :
            self.driver.get(url)
        except TimeoutException as e:
            print(f"Exception encountered: {e}")
            return False
        
    def quit(self) :
        self.driver.quit()
        
    def add_cookies(self, cookies, domain) :
        for i in range(len(cookies)) :
            cookies[i]['domain'] = domain
            try :
                self.driver.add_cookie(cookies[i])
            except :
                pass

    def get_cookies(self) :
        cookies = self.driver.get_cookies()
        return cookies

    def add_xpi_files(self, xpi_file_paths: list) :
        for path in xpi_file_paths:
            try:
                self.driver.install_addon(path)
            except FileNotFoundError:
                print(f"File not found: {path}")

    def execute_java_script(self, script) :
        return self.driver.execute_script(script)
