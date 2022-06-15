import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from townwork.items import TownworkItem
import datetime, re

salaryReHour = re.compile(r"時給(.+?)円")
salaryReMonth = re.compile(r"月給(.+?)円")

def getSalary(salaryStr):

    resHour = re.search(salaryReHour,salaryStr)
    resMonth = re.search(salaryReMonth,salaryStr)
    salaryNmHour, salaryNmMonth = None, None

    if resHour:
        salaryNmHour = resHour.group(1)
    if resMonth:
        salaryNmMonth = resMonth.group(1)

    return salaryNmHour, salaryNmMonth


class KeywordsindeedSpider(scrapy.Spider):
    
    name = 'townwork'
    allowed_domains = ['townwork.net']
    
    def start_requests(self):

        start_urls = [
            # 梅津　飲食
            # 'https://townwork.net/joSrchRsltList/?jc=001&ac=041',
            # 梅津　警備
            # 'https://townwork.net/joSrchRsltList/?jmc=01007&ac=041&ds=01',
            # 中山　介護・保育
            # 'https://townwork.net/joSrchRsltList/?jmc=01511&jmc=01506&jmc=01510&jmc=01512&jmc=01517&jmc=01518&jmc=01403&jmc=01520&ac=041&ds=01',
            # 販売
            # 'https://townwork.net/joSrchRsltList/?jc=002&ac=041&ds=01',
            # レジャー・エンタメ
            # 'https://townwork.net/joSrchRsltList/?jc=011&ac=041&ds=01',
            # 石井　事務
            # 'https://townwork.net/joSrchRsltList/?jc=003&ac=041&ds=01',
            # 梅津　「給食補助」
            # 'https://townwork.net/joSrchRsltList/?fw=%E7%B5%A6%E9%A3%9F&ac=041&ds=01',
            # 物流
            # 'https://townwork.net/joSrchRsltList/?jc=012&ac=041&ds=01',
            # 軽作業
            #'https://townwork.net/joSrchRsltList/?jc=018&ac=041&ds=03',
            # 建築
            # 'https://townwork.net/joSrchRsltList/?jc=013&jc=019&ac=041&ds=01',
            # IT
            # 'https://townwork.net/joSrchRsltList/?jc=005&ac=041&ds=01',
            # 芸能・専門職
            # 'https://townwork.net/joSrchRsltList/?jc=008&jc=017&ac=041&ds=01',
            # 枠マスター　介護助手
            # 'https://townwork.net/tokyo/jc_015/jmc_01518/',
            # 'https://townwork.net/joSrchRsltList/?jc=001&ac=041',
            # 中山　アパレル
            #"https://townwork.net/joSrchRsltList/?jmc=00202&ac=041&ds=01",
            # 梅津　飲食以外新着
            # "https://townwork.net/joSrchRsltList/?ac=041&jc=002&jc=010&jc=011&jc=009&jc=003&jc=004&jc=014&jc=012&jc=018&jc=013&jc=019&jc=005&jc=015&jc=007&jc=008&jc=020&jc=017&ds=03",
            # 梅津 警備、建築
            # "https://townwork.net/joSrchRsltList/?jmc=01007&jc=013&ac=041&ds=03",
            # 渡邉　軽作業、土木、建築
            # "https://townwork.net/joSrchRsltList/?ac=041&jc=018&jc=013&ds=03",
            # CL Nagoya 接客・レジャー・営業・事務・総務すべて　新着順 220527 4859件
            # "https://townwork.net/joSrchRsltList/?mac=08100&jc=010&jc=011&jc=009&jc=003&jc=004&ds=03",
            # 札幌一般事務
            "https://townwork.net/joSrchRsltList/?mac=10100&jmc=00303&emc=01&emc=06&emc=02&ds=03",
                     ]
        # 20 records/page
        for p in list(range(2,6)):
            start_urls.append(f'https://townwork.net/joSrchRsltList/?mac=10100&jmc=00303&emc=01&emc=06&emc=02&ds=03&page={p}')
        
        for url in start_urls:
            
            yield scrapy.Request(url=url, callback=self.parse)
        



    
        
    def parse(self, response):
        
        cards = response.xpath('//div[@class="job-lst-main-cassette-wrap"]')
        
        for card in cards:
            
            item = TownworkItem()
            
            detailedUrl =  'https://townwork.net' + card.xpath('.//div[@class="job-lst-box-wrap"]/a').attrib['href']
            
            
            """ 枠マスター原稿用

                        
            yield scrapy.Request(detailedUrl,
                                 callback=self.parse_detail,
                                 meta={'item':item})
            """            
            
            """ 一般用 """
            
            #if "joid_U" in detailedUrl:# 枠原稿飛ばす。少なすぎる
            #    continue
                
            item['today'] = datetime.date.today()
            
            try:# 新着案件用、でないとtimelimitないやつ取れない。逆に掲載終了案件欲しいときはつけないと量が膨大？
                item['timelimit'] = "掲載終了：" + card.xpath('.//p[@class="job-lst-main-period-limit"]/span/text()').get()
            except Exception:
                item['timelimit'] = "None"
                
            salaryText = card.xpath('.//table/tbody/tr[1]/td//text()').extract()
            salaryText = "".join([e.strip() for e in salaryText])
            item['salary'] = salaryText
            nmH, nmM = getSalary(salaryText)
            item["salaryNumHour"] = nmH
            item["salaryNumMonth"] = nmM
            
            stationText = card.xpath('.//table/tbody/tr[2]/td//text()').extract()
            item['station'] = "".join([e.strip() for e in stationText])
            
            wtText = card.xpath('.//table/tbody/tr[3]/td//text()').extract()
            item['workingtime'] = "".join([e.strip() for e in wtText])
            
            item['url'] = detailedUrl
                        
            yield scrapy.Request(detailedUrl,
                                 callback=self.parse_detail,
                                 meta={'item':item})

            
    
    def parse_detail(self,response):
        
        item = response.meta['item']
        
        """ 枠マスター原稿用

        item['company'] = response.xpath('.//span[@class="jsc-company-txt"]/text()').get().strip()
        item['title'] = response.xpath('.//span[@class="jsc-job-txt"]/text()').get().strip()
        item['catch'] = response.xpath('.//div[@class="job-detail-caption-c"]/text()').extract()
        item['lead'] = response.xpath('.//dl[@class="job-ditail-tbl-inner"]/dt[contains(text(),"アピール情報")]/following-sibling::dd//text()').extract()
        """
        
        """ 一般用 """
        
        item['company'] = response.xpath('.//span[@class="jsc-company-txt"]/text()').get().strip()
        
        item['occupation'] = response.xpath('.//span[@class="jsc-job-txt"]/text()').get().strip()
        item['title'] = response.xpath('.//div[@class="job-detail-caption-c"]/text()').get()
        # item['subtitle'] = response.xpath('.//p[@class="job-detail-txt"]/text()').get()
        
        loc = response.xpath('.//dl[@class="job-ditail-tbl-inner"]/dt[contains(text(),"勤務地")]/following-sibling::dd//text()').extract()
            
        item['location'] = " ".join([l.strip() for l in loc])

        telNum = response.xpath('.//p[@class="detail-tel-num"]/span/text()').get()
        if telNum == None:
            telNumPre = response.xpath('.//p[@class="detail-tel-ttl"]/span/text()').extract()
            telNum = [t.strip() for t in telNumPre if len(t.strip()) > 0][0]
        
        item['tel'] = telNum

        yield item
