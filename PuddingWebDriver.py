from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.firefox.service import Service
from selenium.webdriver import FirefoxOptions
from selenium import webdriver

import time
import random

from .PuddingProxy import PuddingProxy

#Writen by Pudding and Everlong

class PuddingWebDriver:
    class TabNotFoundError(Exception):
        pass

    class IFrameNotFoundError(Exception) :
        pass

    def __init__(self, options:FirefoxOptions=None, service:Service=None, keep_alive:bool=True, proxy:PuddingProxy=None):
        if proxy :
            local_address, local_port = proxy.launch()
            options.set_preference("network.proxy.type", 1)
            options.set_preference("network.proxy.socks", local_address)
            options.set_preference("network.proxy.socks_port", local_port)

            # set the navigator.geolocation.getCurrentPosition() response to that of the proxies ip address
            options.set_preference("geo.provider.network.url", proxy.get_firefox_geo_data())
            
        self.proxy = proxy
        self.driver = webdriver.Firefox(options=options, service=service, keep_alive=keep_alive)
        self.page_load_timeout = 60

    def wait_for_title(self, title, timeout=40):
        try:
            WebDriverWait(self.driver, timeout).until(lambda x: title in x.title)
            return True
        except TimeoutException :
            return False
        
    def wait_for_title_change(self, current_title=None, timeout=40):
        try:
            if not current_title :
                current_title = self.get_title()
            WebDriverWait(self.driver, timeout).until(lambda x: not (current_title in x.title))
            return True
        except TimeoutException :
            return False

    def click_element(self, identifier, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(identifier))
            element.click()
            return True
        except Exception:
            return False

    def refresh_page(self, timeout=40):
        original_timeout = self.get_page_load_timeout()
        try:
            self.set_page_load_timeout(timeout)
            self.driver.refresh()
            self.set_page_load_timeout(original_timeout)
            return True
        except TimeoutException:
            self.set_page_load_timeout(original_timeout)
            return False
        
    def close_other_tabs(self, tab_index:int=-1):
        '''
        closes all tabs except the specified one or the initial tab if no index is provided. 
        '''
        # Get the current window handle
        initial_window_handle = self.driver.current_window_handle

        # Get all window handles
        all_window_handles = self.driver.window_handles

        if tab_index != -1 :
            # Iterate through the list of window handles and close the tabs that don't match the specified tab index
            for index, window_handle in enumerate(all_window_handles):
                if index != tab_index:
                    self.driver.switch_to.window(window_handle)
                    self.driver.close()
                else :
                    initial_window_handle = window_handle
        else :
            for window_handle in all_window_handles :
                if window_handle != initial_window_handle:
                    self.driver.switch_to.window(window_handle)
                    self.driver.close()
        # Switch back to the remaining window handle
        self.driver.switch_to.window(initial_window_handle)


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
                try :
                    element.send_keys(key)
                except StaleElementReferenceException :
                    element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(identifier))
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
        
    def select_by_value(self, identifier, value) :
        try :
            element = self.driver.find_element(identifier[0], identifier[1])
            selector = Select(element)
            selector.select_by_value(value)
            return True
        except :
            return False
        
    def select_by_index(self, identifier, index) :
        try :
            element = self.driver.find_element(identifier[0], identifier[1])
            selector = Select(element)
            selector.select_by_index(index)
            return True
        except :
            return False
        
    def find_element(self, identifier) -> WebElement :
        try :
            element = self.driver.find_element(identifier[0], identifier[1])
            return element
        except NoSuchElementException :
            return None
        
    def find_elements(self, identifier) -> list[WebElement] :
        return self.driver.find_elements(identifier[0], identifier[1])
            
    def is_element_visible(self, identifier, timeout=10) -> WebElement:
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(identifier))
            return element
        except TimeoutException:
            return False
        
    def is_element_clickable(self, identifier, timeout=10) -> WebElement :
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(identifier))
            return element
        except TimeoutException:
            return False
        
    def is_element_present(self, identifier, timeout=10) -> WebElement :
        try : 
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(identifier))
            return element
        except TimeoutException : 
            return False
        
    def get_attribute(self, element_identifier, attribute:str) :
        try :
            attribute_data = self.driver.find_element(element_identifier[0], element_identifier[1]).get_attribute(attribute)
            return attribute_data
        except : 
            return False
        
    def get_title(self) -> str:
        return self.driver.title
    
    def get_user_agent(self) -> str:
        return self.execute_java_script("return navigator.userAgent")
    
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
    
    def tab_count(self) -> int:
        tab_count = len(self.driver.window_handles)
        return tab_count

    def set_page_load_timeout(self, timeout):
        self.page_load_timeout = timeout
        self.driver.set_page_load_timeout(timeout)

    def get_page_load_timeout(self):
        return self.page_load_timeout

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
        
    def get_new_tab(self, url='') :
        self.driver.switch_to.new_window('tab')
        if url != '' :
            self.get(url)
        
    def current_url(self) -> str:
        return str(self.driver.current_url)
        
    def quit(self) :
        self.driver.quit()
        self.proxy.kill()

    def close(self) :
        self.driver.close()
        
    def add_cookies(self, cookies, domain:str=None) :
        for i in range(len(cookies)) :
            if domain :
                cookies[i]['domain'] = domain
            try :
                self.driver.add_cookie(cookies[i])
            except :
                pass

    def get_cookies(self) :
        cookies = self.driver.get_cookies()
        return cookies
    
    def clear_cookies(self) :
        self.driver.delete_all_cookies()

    def add_xpi_files(self, xpi_file_paths: list) :
        for path in xpi_file_paths:
            try:
                self.driver.install_addon(path)
            except FileNotFoundError:
                print(f"File not found: {path}")

    def execute_java_script(self, script, args=[]) :
        return self.driver.execute_script(script, args)
    
    def get_pid(self) :
        return self.driver.service.process.pid
    
    def switch_iframe(self, identifier) :
        if isinstance(identifier, tuple) :
            target_iframe = self.find_element(identifier)
            if not target_iframe :
                raise self.IFrameNotFoundError(f"The IFrame {identifier} could not be found")
        else :
            target_iframe = identifier
        self.driver.switch_to.frame(target_iframe)

    def get_html(self) :
        return self.driver.page_source

    def switch_to_default_iframe(self) :
        self.driver.switch_to.default_content()

    def update_preferences(self, preferences:list[str, any]) :
        '''
        ### Opens about:config and attempts to add all options.

        ---

        Only works on FireFox, and plz do not use any single quotes

        I dont know why I said plz I don't really care what you do...  but things will break.
        '''
        def preference_string(pref) :
            # Make the script work with any value type
            if type(pref[1]) is bool :
                preference_script = f"Preferences.set('{str(pref[0])}', {str(pref[1]).lower()});\n"
            elif type(pref[1]) is int :
                preference_script = f"Preferences.set('{str(pref[0])}', {pref[1]});\n"
            else :
                preference_script = f"Preferences.set('{str(pref[0])}', '{str(pref[1])}');\n"

            return preference_script
        
        initial_window_handle = self.driver.current_window_handle
        self.get_new_tab('about:config')
        script = 'const { Preferences } = ChromeUtils.import("resource://gre/modules/Preferences.jsm");\n'
        for pref in preferences :
            script += preference_string(pref)

        try :
            self.execute_java_script(script)
            self.close()
            self.driver.switch_to.window(initial_window_handle)
            return True
        except Exception as e :
            print(f'While setting prefrences: {e}')
            self.close()
            self.driver.switch_to.window(initial_window_handle)
            return False
        
    def find_subelement(self, parent:WebElement, identifier) :
        try :
            element = parent.find_element(identifier[0], identifier[1])
            return element
        except NoSuchElementException :
            return None