# RankListCrawl

基于 [Python3](https://www.python.org/downloads/)，[Beautifulsoup4](https://pypi.org/project/beautifulsoup4/) 和 [Openpyxl](https://openpyxl.readthedocs.io/en/stable/) 的简单排行版爬虫，数据会被写入 Excel，可实现并发爬取。

## 使用

- 安装 [Python 3.8](https://www.python.org/downloads/) 和 [Git](https://git-scm.com/downloads)
- 使用 Git 下载项目

```bash
git clone https://github.com/vcheckzen/RankListCrawl.git
```

- 安装依赖

```bash
pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

- 运行项目

```bash
python start.py
```

- 运行结束后，可在 `data` 目录查看生成的 `Excel` 文件

## 开发

### 目录结构

```bash
.
├── LICENSE
├── README.md
├── requirements.txt
├── sites            # 站点包，每个站点都是 utils.crawl.RankCrawl 的子类
│   ├── __init__.py
│   ├── forbes.py    # 福布斯爬虫
│   └── hurun.py     # 胡润爬虫
├── start.py         # 启动文件
└── utils            # 工具包
    ├── __init__.py
    ├── crawl.py     # 爬虫抽象类
    ├── excel.py     # Excel 写入类
    └── extractor.py # 文本提取类
```

如需爬取其他站点，在 `sites` 目录增加对应的 `utils.crawl.RankCrawl` 实现类即可
