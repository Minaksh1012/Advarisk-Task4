from scrapy import Request, FormRequest
from uuid import uuid4
import csv
import scrapy

class colony_data(scrapy.Spider):
    name="colony_data"
    
    def start_requests(self):
        yield Request('http://www.onlineumc.org.in:8080/umc/jsp/propertyduessearch.jsp?id=0&lang=1',
            meta={'cookiejar':str(uuid4)},
            callback=self.parse) 
    
    def parse(self,response):
        # import pdb;pdb.set_trace()
        data=response.xpath('//*[@name="propward"]/option/@value').extract()[1:5]
        # print(data,"+++++++++++++++++++/++++++++")
        for property_no in data:
            # print(property_no,'***************************************************************')
            yield FormRequest('http://www.onlineumc.org.in:8080/umc/jsp/propertyduessearch.jsp',
                formdata = {
                    'txtFName': '',
                    'txtSName':'', 
                    'txtLName':'' ,
                    'oldpropno':'', 
                    'propward': property_no,
                    'lang': "1"},
                    meta={'cookiejar':str(uuid4)},
                    callback=self.next_page)

    def next_page(self,response):
        pages = response.xpath('//*[@class="bluetext"]/td[@class="contentmarathi"]/a/@href').extract()
        for page in pages:
            yield Request('http://www.onlineumc.org.in:8080/umc/jsp/{}'.format(page),
            meta={'cookiejar':str(uuid4)},
            callback=self.pages_data)

    def pages_data(self,response):
        # open('page.html','w').write(response.text)
        # import pdb;pdb.set_trace()


        table=response.xpath('//*[@id="cash"]/table//tr')
        # print(table,"mmmmmmmmmmmmmmm")
        with open('pages.csv','w') as f:
            for td in table.xpath(".//td"):
                for a in td.xpath(".//a/font/text()").extract():
                    f.write(a)
                    f.write("\n")



# from uuid import uuid4
# import scrapy
# import csv

# class PropertiesSpider(scrapy.Spider):
#     name = 'properties_data'

#     def start_requests(self):
#         yield scrapy.Request(
#             url ='http://www.onlineumc.org.in:8080/umc/jsp/propertyduessearch.jsp?id=0&lang=1',
#             callback = self.parse
#         )

#     def parse(self, response):
#         property_numbers = response.xpath('//*[@name="propward"]/option/@value')[1:11].extract()
#         yield scrapy.Request("http://www.onlineumc.org.in:8080/umc/jsp/propertyduessearch.jsp?txtFName=&txtSName=&txtLName=&oldpropno=&propward=4100000005&pageNumber=2",
#             callback=self.next_page)
#         for property_number in property_numbers:
#             yield{
#                 "txtFName":"",
#                 "txtSName":"",
#                 "txtLName":"",
#                 "oldpropno":"",
#                 "propword":property_number,
#                 "lang":"1"
#             }

#     def next_page(self,response):
#         table=response.xpath('//*[@id="cash"]/table/tr')
#         with open('properties_data.csv','w') as f:
#             for td in table.xpath('.//td'):
#                 for a in td.xpath('.//a/font/text()').extract():
#                     f.write(a)
#                     f.write("\n")