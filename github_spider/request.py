# # -*- coding=utf8 -*-
#
# import time
import logging
import requests
from github_spider.middlewares import GithubSpiderDownloaderMiddleware

from github_spider.settings import (
    USER,
    PASS
)


def get_reponse(url):
    try:
        logging.debug('get {}'.format(url))
        response = requests.get(url, auth=(USER, PASS))
        if not response.ok:
            logging.debug('get {} failed'.format(url))
        return response
    except Exception as exc:
        logging.error('get {} fail'.format(url))
        logging.exception(exc)





