import github_spider.request as request
import requests
import sys
import logging
import github_spider.utils as utils
from github_spider.config import (
    FILE_TYPE_FOR_EXTRACTION,
    INCLUDE_WORDS,
    EXCLUDE_WORDS,
    OUTPUT_DIR
)


# check all repos for one user
def download_files(repo_urls):
    for repo_url in repo_urls:
        logging.debug(' ++++++++++++ check repo_urls: {} '.format(repo_url))
        response = request.get_reponse(repo_url).json()
        content_url = response.get('contents_url').split('{')[0]
        extract_file(content_url)


# extract files for a project
def extract_file(content_url):
    response = request.get_reponse(content_url).json()
    for data in response:
        type = data.get('type')
        if type == 'file':
            download_url = data.get('download_url')
            if not FILE_TYPE_FOR_EXTRACTION:
                check_target(download_url)
            else:
                suffix = '.' + download_url.split('.')[-1]
                if suffix in FILE_TYPE_FOR_EXTRACTION:
                    check_target(download_url)
        elif type == 'dir':
            extract_file(data.get('url'))


# check include and exclude keyowords
def check_target(download_url):
    raw_text = requests.get(download_url).text
    if EXCLUDE_WORDS:
        if any(ignored_word in raw_text for ignored_word in EXCLUDE_WORDS):
            return False
    if INCLUDE_WORDS:
        if all(keyword in raw_text for keyword in INCLUDE_WORDS):
            save_file(download_url, raw_text)
            return True
    else:
        save_file(download_url, raw_text)
        return True


# save into local machine
def save_file(download_url, raw_text):
    filepath = download_url.split('.com')[-1]
    save_dir = OUTPUT_DIR + '/'.join(filepath.split('/')[:-1])
    utils.check_output_dir(save_dir)
    save_file = OUTPUT_DIR + filepath
    logging.debug(' ++++++++++++ saved this file: {} '.format(save_file))
    f = open(save_file, 'w+')
    f.write(raw_text)
    f.close()

