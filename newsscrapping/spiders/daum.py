from pathlib import Path
from bs4 import BeautifulSoup
import scrapy
import tqdm
from datetime import datetime as dt

class DaumScrapper(scrapy.Spider):
    name = "DaumScrapper"

    def start_requests(self, date=20221015):
        for pageNum in range(1, 3000):
            # dt.today().strftime('%Y%m%d')
            url = f"https://news.daum.net/breakingnews?page={pageNum}"
            #https://news.daum.net/breakingnews?page=30&regDate=20221016
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # news list based on full xpath 
        # november 7 daum -> /html/body/div[2]/div/div/div[1]/div[2]/ul/li[1]/div -> 
        # for first news of the list
        # /html/body/div[2]/div/div/div[1]/div[2]/ul/li/div -> all news lists
        # news = response.xpath("/html/body/div[2]/div/div/div[1]/div[2]/ul/li/div").getall()
        # news_text = response.xpath("/html/body/div[2]/div/div/div[1]/div[2]/ul/li/div").css("a::text").getall()
        # news_desc = response.xpath("/html/body/div[2]/div/div/div[1]/div[2]/ul/li/div").css("span::text").getall()
        # news_link = response.xpath("/html/body/div[2]/div/div/div[1]/div[2]/ul/li/div").css("a::attr(href)").getall()
        news = response.xpath("/html/body/div[2]/div/div/div[1]/div[2]/ul/li[1]/div").getall()
        for new in news:
              soup = BeautifulSoup(new, "html.parser")
              print(soup)
              yield {
                  "title": soup.find(class_='link_txt').text.strip(),
                  "desc": soup.find(class_="desc_thumb").text.strip(),
                  "url": soup.a['href'],
                #   "date": soup.a['href']
                }
              

# scrapy crawl DaumScrapper -O DaumScrapperV3.json
