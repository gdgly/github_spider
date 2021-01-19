# github_spider

## Description:
 This github spider is used to crawl and download all files with your own filter

## Required Environment:
  - python3 (tested with python 3.8 only)

## HOW TO RUN:
  - ```pip3 install Scrapy```
  - ```pip3 install -r requirements.txt```
  - Modify ```github_spider/settings.py``` for your username and auth token (under https://github.com/settings/developers)
  - Modify ```github_spider/config.py``` for your filter option
  - ```scrapy crawl spider``` to run the spider
  
## Filter:
  - check ```github_spider/config.py```
