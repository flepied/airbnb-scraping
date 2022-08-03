# AirBnb Scraping

## Project Overview

A web scraper for AirBnb. This script will extract information like title, price, rating and bedrooms for a given location and print the result as a json file. You can use it to track your next holiday target or collect data for some analytics.

This project is inspired by [X-technology](https://github.com/x-technology/airbnb-analytics). If you want to get a deeper understanding, visit the blog posts or webinar videos below.

Also be aware that airbnb could change all tag id's inside of file ***airbnb_listing_scraper.py*** so if your extracted file is missing data you need to update them.

## Project Setup

* Clone the repository
* Create a virtual environment and activate it

```ShellSession
$ virtualenv .venv
$ source .venv/bin/activate
```

* Install all required packages

```ShellSession
$ pip install -r requirements.txt
```

* Run airbnb\_listing\_scraper.py with your own url or with the default url and redirect the output to a file:

```ShellSession
$ python airbnb_listing_scraper.py '<url of your query>' ... > results.json
```

* you can then use a json tool like [jq](https://stedolan.github.io/jq/) to explore your data:

```ShellSession
$ jq . results.json
$ jq '.|length' results.json
```

## Server Deployment

Selenium requires a browser like Google-Chrome.

For deployment to a server a headless version of Google-Chrome is required as well as a [ChromeDriver](https://chromedriver.chromium.org/).

Here is a nice guide for installing [Google-Chrome Headless Version](https://www.notion.so/Chromedriver-Error-caa1ab54c6684318bb60a4bc6caac7b5#f48813bee20c44b8963667c41a80b266).

Check your google-chrome version

```ShellSession
$ google-chrome --version
```

Go to the [ChromeDriver](https://chromedriver.chromium.org/) homepage and navigate to the driver file which matches your Chrome version and OS. For example Chrome version 104 (beta) for Linux would be

```ShellSession
$ wget https://chromedriver.storage.googleapis.com/104.0.5112.29/chromedriver_linux64.zip
$ unzip chromedriver_linux64.zip
$ chmod +x chromedriver
```

Test it by including your extracted ChromeDriver path into to following script:

```python
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome('<YOUR_CHROMEDRIVER_PATH>', chrome_options=chrome_options,  service_args=['--verbose'])


driver.get('https://google.org/')
print(driver.title)
```

If you don't see any errors, the installation was successful. Now you have to include the commented part inside the method ***\_\_init\_\_*** on file ***airbnb\_listing\_scraper.py***.

In case you are facing any error messages, please open an issue ticket!
