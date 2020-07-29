import os
import abc
import requests
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup

from utils.excel import ExcelHelper
from utils.extractor import TextExtractor


class Crawl(metaclass=abc.ABCMeta):
    def __init__(self, excel_save_folder):
        self.excel_save_folder = excel_save_folder
        if not os.path.exists(excel_save_folder):
            os.makedirs(excel_save_folder)

    def get_excel(self, excel_file_name):
        return ExcelHelper(self.excel_save_folder, excel_file_name)

    @staticmethod
    def get_soup(url):
        return BeautifulSoup(requests.get(url).text, 'html.parser')

    @staticmethod
    def get_extractor(url):
        return TextExtractor(requests.get(url).text)

    @abc.abstractmethod
    def start(self):
        pass


class RankCrawl(Crawl):
    def __init__(self, excel_save_folder):
        super(RankCrawl, self).__init__(excel_save_folder)

    @abc.abstractmethod
    def extract_rank_lists(self):
        pass

    @abc.abstractmethod
    def extract_rank_table(self, rank_url, rank_name):
        pass

    def start(self):
        (rank_count, rank_link_generator) = self.extract_rank_lists()

        print('Start crawling, {:^2d} total rank lists'.format(rank_count))
        print('{:>4s}  {:<40s}'.format('Left', 'Crawled'))

        futures, pool = [], ThreadPoolExecutor(rank_count)
        for url, name in rank_link_generator:
            futures.append(pool.submit(self.extract_rank_table, url, name))

        for i, future in enumerate(futures):
            print('{:>4d}  {:<40s}'.format(rank_count - i - 1, future.result()))

        print('All tasks finished')
