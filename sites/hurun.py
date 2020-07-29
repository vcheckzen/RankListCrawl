import json
import requests
import datetime
from decimal import Decimal

from utils.crawl import RankCrawl


class HurunCrawl(RankCrawl):
    host_url = 'https://www.hurun.net'

    def __init__(self, excel_save_folder):
        super(HurunCrawl, self).__init__(excel_save_folder)

    class TableFormatter:
        def __init__(self, list_type):
            self.list_type = list_type

        def format_wealth_name(self, wealth_name):
            if not wealth_name:
                return None
            if self.list_type in ['百富榜', '独角兽榜']:
                wealth_name += " (人民币)"
            elif self.list_type in ['全球榜', '印度榜']:
                wealth_name += " (美元)"
            return wealth_name

        @staticmethod
        def to_age(value):
            if not value or value == '/':
                return '/'
            birth_years = value.split('、')
            this_year = datetime.datetime.now().year
            age = ''
            for year in birth_years:
                if year.isdigit():
                    age += str(this_year - int(year))
                else:
                    age += year
                age += '、'
            return age.rstrip('、')

        def b_to_yi(self, value):
            if self.list_type in ['全球榜', '印度榜']:
                value = Decimal(value) * 10
            return str(value)

        def yi_to_b(self, value):
            if self.list_type in ['百富榜', '独角兽榜']:
                value = Decimal(value) / 10
            return str(value)

        @staticmethod
        def format_cha(value):
            if len(value) <= 4:
                return str(Decimal(value) / 1000) + ' 千万'
            return str(Decimal(value) / 10000) + ' 亿'

        @staticmethod
        def format_cha_en(value):
            if len(value) <= 6:
                return str(Decimal(value) / 100) + ' M'
            return str(Decimal(value) / 100000) + ' B'

    class TableExtractor:
        def __init__(self, url):
            self.extractor = HurunCrawl.get_extractor(url)
            self.column_tuple = self.find_column_tuple()
            self.list_type = self.find_list_type()
            self.formatter = HurunCrawl.TableFormatter(self.list_type)
            self.wealth_name = self.formatter.format_wealth_name(self.find_wealth_name())

        def find_list_type(self):
            return self.extractor.find_one(r'name="listtype" value="(.+)" class')

        def find_wealth_name(self):
            return self.extractor.find_one(r'var wealthName = "(.+)"')

        def find_column_tuple(self):
            return self.extractor.find_all(r'title: (.+), field: "(.{,10})"(?:.+return (.+)\((?:.+\+"(.+)")?)?')

        def column_name_generator(self):
            for column in self.column_tuple:
                if column[0] == 'wealthName':
                    yield self.wealth_name
                else:
                    yield column[0].strip('"')

        def column_value_generator(self):
            rank_data_url = HurunCrawl.host_url + self.extractor.find_one(r'url: "(/CN/HuList/.+)"')
            data = json.loads(requests.get(rank_data_url).text)
            formatter_map = {
                'ToAge': self.formatter.to_age,
                'BtoYi': self.formatter.b_to_yi,
                'YitoB': self.formatter.yi_to_b,
                'FormatCha': self.formatter.format_cha,
                'FormatChaEn': self.formatter.format_cha_en,
            }
            for i, elem in enumerate(data):
                column_values = []
                for column in self.column_tuple:
                    v = elem[column[1]]
                    if not column[2] == '':
                        v = formatter_map[column[2]](v) + column[3]
                    column_values.append(v)
                yield i, column_values

    def extract_rank_lists(self):
        soup = self.get_soup(self.host_url + '/CN/HuList/')

        rank_links = []
        for rank_cate in soup.select('.dropdown-item a'):
            rank_cate_url = self.host_url + rank_cate['href']
            rank_soup = self.get_soup(rank_cate_url)
            for option in rank_soup.select('#toolbar option'):
                if not option['value'] == '#':
                    rank_links.append((rank_cate_url.split('?')[0] + option['value'],
                                       option.text + rank_cate.text))

        return len(rank_links), rank_links

    def extract_rank_table(self, rank_url, rank_name):
        excel = self.get_excel(rank_name)
        extractor = self.TableExtractor(rank_url)

        excel.write_sheet_row(1, extractor.column_name_generator())
        for i, values in extractor.column_value_generator():
            excel.write_sheet_row(i + 2, values)

        excel.save()
        return rank_url + ' -> ' + rank_name
