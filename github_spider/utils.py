# -*- coding=utf8 -*-
import os
from github_spider.request import get_reponse
from github_spider.config import (
    GITHUB_API_HOST,
    LANGUAGES
)


def check_output_dir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)


def gen_user_page_url(user_name):
    if type(user_name) == list:
        users = []
        for user in user_name:
            users.append('https://{}/users/{}'.format(GITHUB_API_HOST, user))
        return users
    else:
        # get user github url
        return 'https://{}/users/{}'.format(GITHUB_API_HOST, user_name)


def gen_user_follwer_urls(followers_url):
    results = []
    followers = get_reponse(followers_url).json()
    for data in followers:
        results.append(data.get('url'))
    return results


def gen_user_following_urls(following_url):
    results = []
    following_url = following_url.split('{')[0]
    followings = get_reponse(following_url).json()
    for data in followings:
        results.append(data.get('url'))
    return results


def get_repos(repos_url):
    results = []
    response = get_reponse(repos_url).json()
    for data in response:
        # data.get('languages_url'): to determine language distribution
        if check_language_distribution(data.get('languages_url')):
            results.append(data.get('url'))
    return results


def check_language_distribution(languages_url):
    userd_languages = get_reponse(languages_url).json()
    if all(lang.lower() not in LANGUAGES for lang in userd_languages):
        return False
    return True


def save_file(filename, content):
    f = open(filename, "w+")
    f.write('\n'.join(content))
