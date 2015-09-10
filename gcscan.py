#! /usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
import re
import sys
import requests
import time


class GScan(object):
    # Get data from Google Cache
    # Like the date of the last indexation

    def __init__(self):
        self.source_file = ""  # The file where the URLs are
        self.urls = ""  # Contain URLs from source file
        self.results_urls = []  # List of URLs crawled
        self.results_dates = []  # List of cache dates
        self.urls_max_count = 0

    def extract_urls_from_file(self, source_file):
        i = 0
        file = open(source_file, "r")
        self.urls = file.readlines()
        file.close()
        return self.urls

    def get_urls_results(self, urls_extracted):
        i = 0
        for url in urls_extracted:
            self.results_urls.append(url)
            i = i + 1
        self.urls_max_count = i
        return self.results_urls

    def check_captcha(self, driver, current_url):
        captcha = 1
        driver.get(current_url)
        try:
            driver.find_element_by_id("captcha")
        except:
            captcha = 0
        return captcha

    def unlock_captcha(self, current_url):
        print ("[!] Google ask a captcha, fill it and press Enter to resume the scan")
        driver2 = webdriver.Firefox()
        driver2.get(current_url)
        input()

    def get_cache_date(self, urls_extracted, driver):
        print ("Browser loading...")

        if driver == "firefox":
            driver = webdriver.Firefox()
        elif driver == "ghostJS":
            driver = webdriver.PhantomJS()

        i = 0  # For progression check
        print ("There is " + str(self.urls_max_count) + " URLs ready.")

        for url in urls_extracted:
            error_flag = 0  # The URL is considered as accessible by default
            i = i + 1

            # Prepare Google Cache URL
            google_cache_url = "http://webcache.googleusercontent.com/search?q=cache:" + url \
                               + "&amp;espv=2&strip=0&vwsrc=1"

            # Show the progression
            print ("Check the URL " + str(i) + "/" + str(self.urls_max_count))

            if i > 75:  # We delay the crawl for too many URL, fear the captcha :)
                print ("Please wait 27 sec (avoid captcha)")
                time.sleep(27)

            # Open the cached version of the URL
            driver.get(google_cache_url)

            try:
                # Get header of the page named id="google-cache-hdr"
                header = driver.find_element_by_id("google-cache-hdr").text
            except:
                # If the cache doesn't exist, why ?
                error_flag = 1
                status_code = 200  # We consider URL is 200 by default
                test_status_code = ""

                # We try to access the page directly by it's URL
                try:
                    test_status_code = requests.get(url)
                except:
                    status_code = test_status_code.status_code

                if status_code == 200:  # The page exist but is not cached
                    is_captcha = self.check_captcha(driver, google_cache_url)
                    if is_captcha == 0:
                        self.results_dates.append("No cache")
                    else:
                        self.unlock_captcha(google_cache_url)
                else:  # The page is not accessible (404, 500, etc.)
                    self.results_dates.append("Error " + str(status_code))

            if error_flag == 0:  # If the page is well cached, we get the cache date
                # Based on french version of Google (google.fr), sorry :(
                # Get the text (date) between the two sections "était affichée le " and " GMT" in results
                header_date = re.findall('\xe9tait affich\xe9e le (.*?) GMT', header)

                cache_date = header_date[0]
                # TODO : La suppression du /n ne marque que sur le dernier élément
                cache_date = cache_date.replace("\n", "")  # Remove the new line break at each URL
                self.results_dates.append(cache_date)

        driver.close()
        return self.results_dates
