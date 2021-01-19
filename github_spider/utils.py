# -*- coding=utf8 -*-
import os
from github_spider.request import get_reponse
from github_spider.const import (
    GITHUB_API_HOST,
    PAGE_SIZE,
)


def check_output_dir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)


def gen_user_page_url(user_name):
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
        results.append(data.get('url'))
    return results


#
# def gen_user_following_url(user_name, page=1):
#     """获取用户关注用户列表url
#     Args:
#         user_name (string): github用户id
#         page (int): 页号
#     """
#     return 'https://{}/users/{}/following?page={}'.format(GITHUB_API_HOST,
#                                                           user_name, page)
#
#
# def gen_user_repo_url(user_name, page=1):
#     """获取用户项目列表url
#     Args:
#         user_name (string): github用户id
#         page (int): 页号
#     """
#     return 'https://{}/users/{}/repos?page={}'.format(GITHUB_API_HOST,
#                                                       user_name, page)
#
#
# def get_short_url(url):
#     """
#     去掉url前面的https://api.github.com/
#     """
#     return url[23:-1]
#
#
# def find_login_by_url(url):
#     """
#     获取url中的用户名
#     """
#     result = urlparse.urlsplit(url)
#     return result.path.split('/')[2]
#
#
def gen_url_list(user_name, func, count):
    result = []
    page = 1
    while (page - 1) * PAGE_SIZE < count:
        result.append(func(user_name, page))
        page += 1
    return result


# def check_url_visited(urls):
#     """
#     判断url是否重复访问过
#     """
#     result = []
#     for url in urls:
#         short_url = get_short_url(url)
#         visited = redis_client.sismember(REDIS_VISITED_URLS, short_url)
#         if not visited:
#             result.append(url)
#     return result


# def get_proxy():
#     """
#     从redis获取代理
#     """
#     available_proxy = redis_client.zrangebyscore(PROXY_KEY, 0, PROXY_USE_COUNT)
#     if available_proxy:
#         return available_proxy[0]
#     return None

