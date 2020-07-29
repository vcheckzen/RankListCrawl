from sites.forbes import ForbesCrawl
from sites.hurun import HurunCrawl

if __name__ == "__main__":
    ForbesCrawl('./data/Forbes Rank Lists/').start()
    HurunCrawl('./data/Hurun Rank Lists/').start()
