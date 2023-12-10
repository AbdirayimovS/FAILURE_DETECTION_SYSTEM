from pathlib import Path
from bs4 import BeautifulSoup
import scrapy
import tqdm
from datetime import datetime as dt

class DaumScrapper(scrapy.Spider):
    name = "NaverScrapper"

    def start_requests(self):
        today = dt.today().strftime('%Y%m%d')

        for pageNum in range(1, 1500):
            url = f"https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=&date={today}&page={pageNum}"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        news = response.xpath("/html/body/div[1]/table/tbody/tr/td[2]/div/div[2]/ul[1]/li").getall()
        for new in news:
              soup = BeautifulSoup(new, "html.parser")
              yield {
                  "title": soup.a.text.strip(),
                  "desc": soup.find(class_="desc_thumb").text.strip(),
                  "url": soup.a['href'],
                  "date": soup.a['href']
                }
              

# scrapy crawl DaumScrapper -O DaumScrapperV3.json
