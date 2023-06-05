
A util class for selenium webdrivers so you have more time to focus on more important matters, like taco quality and world domination.

## Features


* Wait for a specific title, timeout, or alert

* Click elements with specified identifiers

* Refresh pages

* Send keys to elements

* Switch between tabs

* Set page load timeout

* Handle alerts (accept or dismiss)

* Sleep or sleep within a random range

* Get URLs

* Add cookies to the WebDriver

* Add XPI files

* Switch between forward and back navigation

### Usage
___

```py
from pudding_webdriver import PuddingWebDriver

driver = PuddingWebDriver(driver=webdriver)
driver.wait_for_title("Example Title", timeout=40)
driver.click_element((By.ID, "identifier"), timeout=10)
driver.refresh_page()
driver.send_keys((By.ID, "identifier"), keys, timeout=10)
driver.back()
driver.forward()
driver.switch_tab(tab_index)
driver.set_page_load_timeout(timeout)
driver.handle_alert(accept=True)
driver.sleep(seconds)
driver.sleep_range(min_seconds, max_seconds)
driver.get(url)
driver.add_cookies(cookies, domain)
driver.add_xpi_files(xpi_file_paths: list)
```

#### Yes this was write by an ai ; p
