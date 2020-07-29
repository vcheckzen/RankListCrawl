from utils.crawl import RankCrawl


class ForbesCrawl(RankCrawl):
    def __init__(self, excel_save_folder):
        super(ForbesCrawl, self).__init__(excel_save_folder)
        self.host_url = 'https://www.forbeschina.com'

    def extract_rank_lists(self):
        soup = self.get_soup(self.host_url + '/lists/')
        rank_links = soup.select('.col-lg-4 a')
        return len(rank_links), (
            (self.host_url + rank_link['href'], rank_link.text)
            for rank_link in rank_links
        )

    def extract_rank_table(self, rank_url, rank_name):
        excel = self.get_excel(rank_name)
        soup = self.get_soup(rank_url)

        table = soup.select_one('#data-view')
        excel.write_sheet_row(1, (th.text for th in table.select('thead tr th')))
        for i, tr in enumerate(table.select('tbody tr')):
            excel.write_sheet_row(i + 2, (td.text for td in tr.select('td')))

        excel.save()
        return rank_url + ' -> ' + rank_name
