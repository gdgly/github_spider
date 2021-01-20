import scrapy
import logging
from github_spider.settings import START_USER
import github_spider.utils as utils
import github_spider.spiders.flow as flow
import sys
from scrapy.exceptions import CloseSpider
from github_spider.settings import (
    USER, PASS
)
from github_spider.config import (
    OUTPUT_DIR, MAX_USERS
)


visited_users = []

# main function
class SpiderSpider(scrapy.Spider):
    name = 'spider'
    http_user = USER
    http_pass = PASS
    utils.check_output_dir(OUTPUT_DIR)
    user_url = utils.gen_user_page_url(START_USER)
    start_urls = [user_url]

    def parse(self, response):
        # extract important variables
        json_data = response.json()
        # print(json_data)
        data = {
            'id': json_data.get('login'),
            'repos_count': json_data.get('public_repos', 0),
            'followers': json_data.get('followers_url'),
            'following': json_data.get('following_url'),
            'repos_url': json_data.get('repos_url')
        }
        # check max limit
        visited_users.append(data['id'])
        number_of_visited = len(visited_users)
        if number_of_visited > MAX_USERS:
            visited_users.pop()
            # self.logger.info(" ++++++++++++ Visited users %s", visited_users)
            # self.logger.info(" reached MAX_USERS limit: %s", MAX_USERS)
            utils.save_file(OUTPUT_DIR + "/visited_users.txt", visited_users)
            raise CloseSpider('reached MAX_USERS limit')

        # work START
        next_urls = utils.gen_user_follwer_urls(data['followers'])
        following_urls = utils.gen_user_following_urls(data['following'])
        next_urls += (x for x in following_urls if x not in next_urls)

        logging.debug(' ++++++++++++ next_urls:  {} '.format(next_urls))
        repo_urls = utils.get_repos(data['repos_url'])
        logging.debug(' ++++++++++++ repo_urls:  {} '.format(repo_urls))
        flow.download_files(repo_urls)
        # work END
        # raise CloseSpider('reached MAX_USERS limit')
        # sys.exit(0)
        for i, next_url in enumerate(next_urls):
            try:
                yield response.follow(next_url, callback=self.parse)
            except Exception as exc:
                logging.error(' +++ get failed: {}'.format(next_url))
                logging.exception(exc)

