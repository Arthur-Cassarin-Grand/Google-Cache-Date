# Google-Cache-Date
Get the Google cache date from a list of URLs stored in an plain text file.

Modules used : Selenium, GhostJS and requests.

## Features

* Show Google Cache date for URLs in a file text (ex : from a Screaming Frog SEO Excel File).
* Get the date from text cached version, which is super fast.
* Support : the page exist (HTTP 200) but have no cache.
* Support : the page doesn't exist and return HTTP status.

Note : support only google.fr for the moment, most coming.

## How it works ?

1. Create an "urls.txt" file in the script current directory.
2. Set 1 URL per line.
3. Start the script.

Currently there is no GUI only console interface.

## What we get ?

Two arrays :
* 1 of the URLs scanned.
* 2 of the Google cade dates (same index).

## Documentations

### Class GCScan

#### Methods :

``` python
extract_urls_from_file(source_file)
get_urls_results(urls_extracted)
get_cache_date(urls_extracted, driver)

# The "driver" argument can take two values :
# - "firefox" : firefox is used to get the cache date, require a desktop environnement (only useful for testing).
# - "ghostJS" : headless browser, faster and invisible for the user, perfect for this script.
```

#### Attributes :

``` python
source_file = ""  # The file where the URLs are
urls = ""  # Contain URLs from source file
results_urls = []  # List of URLs crawled
results_dates = []  # List of cache dates
```
