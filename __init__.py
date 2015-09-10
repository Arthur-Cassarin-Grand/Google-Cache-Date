#! /usr/bin/python
# -*- coding: utf-8 -*-

from gcscan import GScan

scan = GScan()
urls = scan.extract_urls_from_file("urls.txt")
array_results_urls = scan.get_urls_results(urls)
array_results_dates = scan.get_cache_date(urls, "firefox")
print (array_results_urls)
print (array_results_dates)