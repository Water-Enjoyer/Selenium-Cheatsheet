from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService


def main(driver):

    # go to page
    url = "https://google.com"
    driver.get(url)

    # webdriver wait
    try:
        search_bar = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[title='Search']")))
    except TimeoutException:
        return

    # simple click
    search_bar.click()

    # send keys
    search_bar.send_keys("dihydrogen monoxide")

    # xpath
    search_button = driver.find_element(By.XPATH, "(//input[@name='btnK'])[2]")

    # sending click through js
    driver.execute_script("arguments[0].click();", search_button)

    # get search results
    search_results = driver.find_element(By.CSS_SELECTOR, "#search")

    # get list of link elements
    link_elems = search_results.find_elements(By.CSS_SELECTOR, "a")

    # get list of link strings
    # links = [elem.get_attribute("href") for elem in search_results.find_elements(By.CSS_SELECTOR, "a")]

    for link in link_elems[:10]:

        # get link url for later to avoid stale element
        link_url = link.get_attribute('href')

        # opens in new tab
        ActionChains(driver) \
            .key_down(Keys.CONTROL) \
            .click(link) \
            .key_up(Keys.CONTROL) \
            .perform()

        # switches to new (second [1]) tab
        driver.switch_to.window(driver.window_handles[1])

        # find all text on page
        all_text = driver.find_element(By.XPATH, "//*").text

        # look for text in page
        if "water" in all_text.lower():
            print(f"Found Water! -> {link_url}")
        else:
            print(f"They're keeping the secret! -> {link_url}")

        # close tab
        driver.close()

        # switch back to original tab
        driver.switch_to.window(driver.window_handles[0])


if __name__ == '__main__':
    # options to clean up terminal output
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # option to start chrome headless to not show browser
    # options.add_argument('--headless')

    # start chromedriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # use stealth
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True
            )

    main(driver=driver)

    driver.quit()
