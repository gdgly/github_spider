import scrapy
from github_spider.settings import START_USER
import github_spider.utils as utils
import github_spider.spiders.flow as flow
from github_spider.settings import (
    USER,
    PASS
)
from github_spider.config import OUTPUT_DIR


# main function
class SpiderSpider(scrapy.Spider):
    name = 'spider'
    http_user = USER
    http_pass = PASS
    utils.check_output_dir(OUTPUT_DIR)
    user_url = utils.gen_user_page_url(START_USER)
    # redis_client.delete(REDIS_VISITED_URLS)
    start_urls = [user_url]
    # xzhou29:a05ca5f8b8d2c763ab87422f49a984f630faf13e
    print('---------------------- start ----------------------')
    # response = requests.get(user_url, auth=('xzhou29', 'a05ca5f8b8d2c763ab87422f49a984f630faf13e'))

    def parse(self, response):
        response = response.json()
        # print(response)
        data = {
            'id': response.get('login'),
            # 'type': response.get('type'),
            # 'name': response.get('name'),
            # 'company': response.get('company'),
            # 'blog': response.get('blog'),
            # 'location': response.get('location'),
            # 'email': response.get('email'),
            'repos_count': response.get('public_repos', 0),
            # 'gists_count': response.get('public+gists', 0),
            'followers': response.get('followers_url'),
            'following': response.get('following_url'),
            # 'created_at': response.get('created_at'),
            'repos_url': response.get('repos_url')
        }

        # follower_urls = utils.gen_user_follwer_urls(data['followers'])
        # following_urls = utils.gen_user_following_urls(data['following'])

        repo_urls = utils.get_repos(data['repos_url'])
        print(repo_urls)
        flow.download_files(repo_urls)

        # user = user or data[0].get('owner', {}).get('login')
        print('---------------------- finished ----------------------')

