# -*- coding: utf-8 -*-

import atexit
import json
import os
import shutil
import sys
import tempfile
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class AirbnbPageScraper:
    def __init__(self):
        self.PATH = "chromedriver"
        tempdir = tempfile.mkdtemp()
        atexit.register(lambda: shutil.rmtree(tempdir))
        chrome_options = webdriver.ChromeOptions()
        # to debug set the NO_HEADLESS env var
        if not os.getenv("NO_HEADLESS"):
            chrome_options.add_argument("--headless")
        # try to avoid side effect from previous sessions
        chrome_options.add_argument(f"--user-data-dir={tempdir}")
        # switching to English doesn't work
        chrome_options.add_argument("--lang=EN")
        self.driver = webdriver.Chrome(
            self.PATH,
            options=chrome_options,
            service_args=["--verbose"],
        )
        self.page = 1

    def get_element_by_class_name(self, elt, name, excpt=False):
        try:
            return elt.find_element(By.CLASS_NAME, name)
        except NoSuchElementException:
            if excpt is True:
                raise NoSuchElementException
            else:
                print(f"Unable to find element with name: {name}", file=sys.stderr)

    def get_element_by_xpath(self, elt, xpath, excpt=False):
        try:
            return elt.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            if excpt is True:
                raise NoSuchElementException
            else:
                print(f"Unable to find element for xpath: {xpath}", file=sys.stderr)

    def get_info(self, url):
        print(f"Scraping {url}...", file=sys.stderr)
        self.driver.get(url)
        # Parse data out of the page
        ret = {}
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.driver.maximize_window()
        # waiting for an element of the page to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@data-testid='inline-availability-calendar']")
                )
            )
        except TimeoutException:
            print("Unable to load page in 10s. Exiting.", file=sys.stderr)
            return ret
        self.accept_cookie_policy()
        self.activate_date_selector()
        self.get_availability(ret)
        self.go_to_next_month()
        self.go_to_next_month()
        self.get_availability(ret)
        self.go_to_next_month()
        self.go_to_next_month()
        self.get_availability(ret)
        return ret

    def accept_cookie_policy(self):
        # click cookie policy
        try:
            button = self.driver.find_element(By.CLASS_NAME, "_148dgdpk")
            self.driver.execute_script("arguments[0].click();", button)
        except NoSuchElementException:
            pass

    def activate_date_selector(self):
        # find the date selector
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@data-testid='change-dates-checkIn']")
                )
            )
        except TimeoutException:
            print("Unable to load page in 10s. Exiting.", file=sys.stderr)
            return
        link = self.get_element_by_xpath(
            self.driver, "//div[@data-testid='change-dates-checkIn']"
        )
        self.driver.execute_script("arguments[0].click();", link)

    def get_availability(self, ret):
        time.sleep(1)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//td/div[contains(@data-testid, 'calendar-day-')]")
                )
            )
        except NoSuchElementException:
            pass
        elements = self.driver.find_elements(
            By.XPATH, "//td/div[contains(@data-testid, 'calendar-day-')]"
        )
        print(len(elements))
        for elt in elements:
            ret[elt.get_attribute("data-testid").split("-")[2]] = (
                elt.get_attribute("data-is-day-blocked") == "true"
            )

    def go_to_next_month(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//button[@aria-label='Avancez pour passer au mois suivant.']",
                    )
                )
            )
        except TimeoutException:
            print("Unable to find next dates button", file=sys.stderr)
            return
        button = self.driver.find_element(
            By.XPATH, "//button[@aria-label='Avancez pour passer au mois suivant.']"
        )
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(1)

    def quit(self):
        self.driver.close()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        urls = [
            "https://www.airbnb.com/s/Estepona--Spain/homes?flexible_trip_lengths%5B%5D=one_week&refinement_paths%5B%5D=%2Fhomes&tab_id=home_tab&date_picker_type=calendar&adults=6&source=structured_search_input_header&checkin=2022-09-10&checkout=2022-09-17",
        ]
    else:
        urls = sys.argv[1:]
    scraper = AirbnbPageScraper()
    for url in urls:
        ret = scraper.get_info(url)
        print(json.dumps(ret))
    if not os.getenv("NO_QUIT"):
        scraper.quit()
