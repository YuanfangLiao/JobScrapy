# JobScrapy
用Scrapy写的一个爬取51job上职位信息的爬虫小软件，爬到的数据可以存到mysql或者mongodb里面


使用方法 先修改pipelines里面的数据库设置，如果不要用数据库的话，就把settings里面对应的pipline注释掉，然后cd到项目目录下
使用命令： scrapy crawl 51job --nolog -a -place="上海" -a -kw="java"  来开始爬取

