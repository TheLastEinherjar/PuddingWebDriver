# PuddingWebDriver:
Welcome to the world of PuddingWebDriver, where tacos, robots, and death rays coexist in harmony. This Python script is designed to push the boundaries of conventional science and help automate your "web browsing" experience.

## Features



- **Wait for Title**: Wait for a specific title to appear in the browser tab.
- **Click Element**: Click on an element identified by a given identifier.
- **Refresh Page**: Refresh the current page.
- **Close Other Tabs**: Close all tabs except for the specified tab index.
- **Send Keys**: Enter text into an input element identified by a given identifier.
- **Type Keys**: Type a series of keys into an input element with optional time delays between each key.
- **Clear Element**: Clear the content of an input element identified by a given identifier.
- **Find Element**: Find a single element identified by a given identifier.
- **Find Elements**: Find multiple elements identified by a given identifier.
- **Check Element Visibility**: Check if an element identified by a given identifier is visible.
- **Check Element Clickability**: Check if an element identified by a given identifier is clickable.
- **Get Attribute**: Get the value of a specified attribute of an element identified by a given identifier.
- **Get Page Title**: Get the title of the current page.
- **Navigate Back**: Go back to the previous page.
- **Navigate Forward**: Go forward to the next page.
- **Maximize Window**: Maximize the browser window.
- **Switch Tab**: Switch to a specific tab by index.
- **Set Page Load Timeout**: Set the timeout for page load operations.
- **Get Page Load Timeout**: Get the current page load timeout value.
- **Handle Alert**: Handle alerts by accepting or dismissing them.
- **Sleep**: Pause the script execution for a specified number of seconds.
- **Sleep Range**: Pause the script execution for a random duration within a specified range.
- **Navigate to URL**: Open a specified URL in the browser.
- **Quit WebDriver**: Quit the WebDriver and close the browser.
- **Add Cookies**: Add cookies to the current session.
- **Get Cookies**: Retrieve all cookies from the current session.
- **Add XPI Files**: Install Firefox add-ons (XPI files) to the current browser session.
- **Execute JavaScript**: Execute custom JavaScript code in the browser.
- **Switch IFrame**: Switch to an iframe identified by a given identifier.
- **Get HTML**: Get the HTML source code of the current page.
- **Switch to Default IFrame**: Switch back to the default content of the page.
- **Update Preferences**: Opens about:config and sets the new preferences.
- **And More That I don't Feel Like Adding ;p**

## Usage


1. Import the `PuddingWebDriver` class from the script.
2. Create an instance of `PuddingWebDriver`, providing a Selenium WebDriver object as the argument.
3. Use the various methods and functionalities provided by `PuddingWebDriver` to enhance your web automation tasks.

## Example:
___

```py
from selenium import webdriver
from selenium.webdriver.common.by import By
from pudding_webdriver import PuddingWebDriver

# Create a Selenium WebDriver instance
driver = webdriver.Chrome()

# Create an instance of PuddingWebDriver
pudding_driver = PuddingWebDriver(driver)

# Wait for a specific title
pudding_driver.wait_for_title("Example Title", timeout=40)

# Click on an element identified by ID
pudding_driver.click_element((By.ID, "identifier"), timeout=10)

# Refresh the current page
pudding_driver.refresh_page()

# Enter text into an input element identified by ID
pudding_driver.send_keys((By.ID, "identifier"), "keys", timeout=10)

# Navigate back to the previous page
pudding_driver.back()

# Navigate forward to the next page
pudding_driver.forward()

# Switch to a specific tab by index
pudding_driver.switch_tab(tab_index)

# Set the page load timeout
pudding_driver.set_page_load_timeout(timeout)

# Handle an alert by accepting it
pudding_driver.handle_alert(accept=True)

# Pause the script execution for a specified number of seconds
pudding_driver.sleep(seconds)

# Pause the script execution for a random duration within a specified range
pudding_driver.sleep_range(min_seconds, max_seconds)

# Open a specified URL in the browser
pudding_driver.get(url)

# Add cookies to the current session
pudding_driver.add_cookies(cookies, domain)

# Install Firefox add-ons (XPI files) to the current browser session
pudding_driver.add_xpi_files(xpi_file_paths)

# Quit the WebDriver
pudding_driver.quit()
```

> Yes this was write by an ai ;p
