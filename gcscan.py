#! /usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
import re
import requests

class GScan(object):
    # Get data from Google Cache
    # Like the date of the last indexation

    def __init__(self):
        self.source_file = ""  # The file where the URLs are
        self.urls = ""  # Contain URLs from source file
        self.results_urls = []  # List of URLs crawled
        self.results_dates = []  # List of cache dates

    def extract_urls_from_file(self, source_file):
        file = open(source_file, "r")
        self.urls = file.readlines()
        file.close()
        return self.urls

    def get_urls_results(self, urls_extracted):
        for url in urls_extracted:
            self.results_urls.append(url)
        return self.results_urls

    def get_cache_date(self, urls_extracted, driver):
        if driver == "firefox":
            driver = webdriver.Firefox()
        elif driver == "ghostJS":
            driver = webdriver.PhantomJS()

        for url in urls_extracted:
            error_flag = 0  # The URL is considered as accessible by default

            # Prepare Google Cache URL
            google_cache_url = "http://webcache.googleusercontent.com/search?q=cache:" + url \
                               + "&amp;espv=2&strip=0&vwsrc=1"

            # Open the cached version of the URL
            driver.get(google_cache_url)

            try:
                # Get header of the page named id="google-cache-hdr"
                header = driver.find_element_by_id("google-cache-hdr").text
            except:
                # If the cache doesn't exist, why ?
                error_flag = 1
                status_code = 200  # We consider URL is 200 by default

                # We try to access the page directly by it's URL
                try:
                    test_status_code = requests.get(url)
                except:
                    status_code = test_status_code.status_code

                if status_code == 200:  # The page exist but is not cached
                    self.results_dates.append("No cache")
                else:  # The page is not accessible (404, 500, etc.)
                    self.results_dates.append("Error " + str(status_code))

            if error_flag == 0:  # If the page is well cached, we get the cache date
                # Based on french version of Google (google.fr), sorry :(
                # Get the text (date) between the two sections "était affichée le " and " GMT" in results
                header_date = re.findall('\xe9tait affich\xe9e le (.*?) GMT', header)

                cache_date = header_date[0]
                # TODO : La suppression du /n ne marque que sur le dernier élément
                cache_date = cache_date.replace("\n","")  # Remove the new line break at each URL
                self.results_dates.append(cache_date)

        driver.close()
        return self.results_dates
