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


class AirbnbListingScraper:
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
        ret = []
        while True:
            print(f"Page {self.page}", file=sys.stderr)
            self.driver.execute_script("window.scrollTo(0, 0);")
            # waiting for an element of the page to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "to8eev7"))
                )
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "c4mnd7m"))
                )
            except TimeoutException:
                print("Unable to load page in 10s. Exiting.", file=sys.stderr)
                break
            # click cookie policy
            try:
                self.driver.find_element(By.CLASS_NAME, "_148dgdpk").click()
            except NoSuchElementException:
                pass
            # parse listing elements
            elements = self.driver.find_elements(By.CLASS_NAME, "c4mnd7m")
            for element in elements:
                info = {"page": self.page}
                has_beds = True
                info["url"] = (
                    self.get_element_by_class_name(element, "ln2bl2p")
                    .get_attribute("href")
                    .split("?")[0]
                )
                print(f"Processing {info['url']}", file=sys.stderr)
                info["type"] = self.get_element_by_class_name(
                    element, "t1jojoys"
                ).text.split(" ⋅ ")[0]
                # some listings do not display beds and bedrooms but dates instead
                try:
                    info["beds"] = int(
                        self.get_element_by_xpath(
                            element,
                            "//div[contains(@class, 'f15liw5s s1cjsi4j')]/span[1]/span",
                        ).text.split(" ")[0]
                    )
                except (ValueError, NoSuchElementException):
                    has_beds = False
                try:
                    info["bedrooms"] = int(
                        self.get_element_by_xpath(
                            element,
                            "//div[contains(@class, 'f15liw5s s1cjsi4j')]/span[2]/span[3]",
                            True,
                        ).text.split(" ")[0]
                    )
                except (ValueError, NoSuchElementException):
                    pass
                if has_beds:
                    info["host_type"] = self.get_element_by_xpath(
                        element, "//div[contains(@class, 'g1tup9az')]/div[4]/span/span"
                    ).text
                else:
                    info["host_type"] = self.get_element_by_xpath(
                        element, "//div[contains(@class, 'g1tup9az')]/div[3]/span/span"
                    ).text
                info["price"] = int(
                    self.get_element_by_class_name(element, "_tyxjp1")
                    .text.split(" €")[0]
                    .replace(" ", "")
                    .replace("\u202f", "")
                )
                try:
                    info["special"] = self.get_element_by_class_name(
                        element, "t1mwk1n0", True
                    ).text
                except NoSuchElementException:
                    pass
                e = self.get_element_by_class_name(element, "ru0q88m").text
                if e.find("(") != -1:
                    note, number = e.split(" (")
                    info["note"] = float(note.replace(",", "."))
                    info["reviews"] = int(number[:-1])
                else:
                    info["note"] = e
                ret.append(info)
            try:
                next_button = self.get_element_by_xpath(
                    self.driver, "//a[contains(@class, '_1bfat5l')]", True
                )
            except NoSuchElementException:
                break
            next_button.click()
            time.sleep(2)
            self.page += 1
        return ret

    def quit(self):
        self.driver.close()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        urls = [
            "https://www.airbnb.com/s/Estepona--Spain/homes?flexible_trip_lengths%5B%5D=one_week&refinement_paths%5B%5D=%2Fhomes&tab_id=home_tab&date_picker_type=calendar&adults=6&source=structured_search_input_header&checkin=2022-09-10&checkout=2022-09-17",
        ]
    else:
        urls = sys.argv[1:]
    scraper = AirbnbListingScraper()
    for url in urls:
        ret = scraper.get_info(url)
        print(json.dumps(ret))
    if not os.getenv("NO_QUIT"):
        scraper.quit()
