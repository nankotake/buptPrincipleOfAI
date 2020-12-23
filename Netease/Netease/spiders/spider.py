import scrapy
from Netease.Netease.items import NeteaseItem

class NetEaseSpider(scrapy.spiders.Spider):
    name = 'NE'
    url_list = {'国内': ['https://temp.163.com/special/00804KVA/cm_guonei.js?callback=data_callback',
                       'https://temp.163.com/special/00804KVA/cm_guonei_0{}.js?callback=data_callback'],
                '国际': ['https://temp.163.com/special/00804KVA/cm_guoji.js?callback=data_callback',
                       'https://temp.163.com/special/00804KVA/cm_guoji_0{}.js?callback=data_callback'],
                '军事': ['https://temp.163.com/special/00804KVA/cm_war.js?callback=data_callback',
                       'https://temp.163.com/special/00804KVA/cm_war_0{}.js?callback=data_callback'],
                '航空': ['https://temp.163.com/special/00804KVA/cm_hangkong.js?callback=data_callback&a=2',
                       'https://temp.163.com/special/00804KVA/cm_hangkong_0{}.js?callback=data_callback&a=2'],
                '科技': ['https://tech.163.com/special/00097UHL/tech_datalist.js?callback=data_callback',
                       'https://tech.163.com/special/00097UHL/tech_datalist_0{}.js?callback=data_callback']}