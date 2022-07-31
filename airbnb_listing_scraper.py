# -*- coding: utf-8 -*-

import json

from selenium import webdriver
from selenium.webdriver.common.by import By


class AirbnbListingScraper:
    def __init__(self):
        self.PATH = "chromedriver"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        #        chrome_options.add_argument("--lang=EN")
        self.driver = webdriver.Chrome(
            self.PATH,
            options=chrome_options,
            service_args=["--verbose"],
        )

    def get_info(self, url):
        ret = self.driver.get(url)
        # Parse data out of the page
        ret = []
        elements = self.driver.find_elements(By.CLASS_NAME, "c4mnd7m")
        for element in elements:
            info = {}
            info["url"] = (
                element.find_element(By.CLASS_NAME, "ln2bl2p")
                .get_attribute("href")
                .split("?")[0]
            )
            info["type"] = element.find_element(By.CLASS_NAME, "t1jojoys").text.split(
                " ⋅ "
            )[0]
            info["beds"] = int(
                element.find_element(
                    By.XPATH,
                    "//div[contains(@class, 'f15liw5s s1cjsi4j')]/span[1]/span",
                ).text.split(" ")[0]
            )
            info["bedrooms"] = int(
                element.find_element(
                    By.XPATH,
                    "//div[contains(@class, 'f15liw5s s1cjsi4j')]/span[2]/span[3]",
                ).text.split(" ")[0]
            )
            info["price"] = int(
                element.find_element(By.CLASS_NAME, "_tyxjp1").text.split(" €")[0]
            )
            e = element.find_element(By.CLASS_NAME, "ru0q88m").text
            if e.find("(") != -1:
                note, number = e.split(" (")
                info["note"] = float(note.replace(",", "."))
                info["reviews"] = int(number[:-1])
            else:
                info["note"] = e
            ret.append(info)
        return ret


if __name__ == "__main__":
    urls = [
        "https://www.airbnb.com/s/Estepona--Spain/homes?flexible_trip_lengths%5B%5D=one_week&place_id=ChIJ09n2kaXWDA0RzA0t1sXwS4o&refinement_paths%5B%5D=%2Fhomes&tab_id=home_tab&date_picker_type=calendar&adults=6&source=structured_search_input_header&search_type=filter_change&checkin=2022-09-10&checkout=2022-09-17",
]
    scraper = AirbnbListingScraper()
    for url in urls:
        ret = scraper.get_info(url)
        print(json.dumps(ret))
