from bs4 import BeautifulSoup
from datetime import datetime as dt
soup = BeautifulSoup("""<div class="cont_thumb">\n                <strong class="tit_thumb">\n                    <a href="https://v.daum.net/v/20231108180047922" class="link_txt">롯데칠성, 새 맥주 \'크러시\' 출시…100% 올 몰트</a>\n                    <span class="info_news">뉴시스<span class="txt_bar"> · </span><span class="info_time">18:00</span></span>\n                </strong>\n                <div class="desc_thumb">\n                    <span class="link_txt">\n                        [서울=뉴시스] 이준호 기자 = 롯데칠성음료가 맥주 신제품 \'크러시(KRUSH)\'를 출시한다고 8일 밝혔다. 롯데칠성음료는 개인의 취향과 표현에 대한 관심이 높아진 요즘, ...\n                    </span>\n                </div>\n            </div>""", 'html.parser')

a = dt.today().strftime('%Y%m%d')
print(a)
date = soup.a['href'].split("/")[-1]
# if date.isdigit():
#     print(date)
#     day = date[6:8]
#     date = dt.now().day
#     print(date - int(day))
# print()
# # print(soup.a.text) text
# print(soup.find(class_="desc_thumb").text.strip())
