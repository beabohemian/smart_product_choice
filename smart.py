from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# 1단계 네이버 쇼핑 검색 순위 크롤링
# 네이버 쇼핑 링크들(카테고리별)
패션의류 = "https://search.shopping.naver.com/best100v2/detail.nhn?catId=50000000"
패션잡화 = "https://search.shopping.naver.com/best100v2/detail.nhn?catId=50000001"
화장품_미용 = "https://search.shopping.naver.com/best100v2/detail.nhn?catId=50000002"
디지털_가전 = "https://search.shopping.naver.com/best100v2/detail.nhn?catId=50000003"
가구_인테리어 = "https://search.shopping.naver.com/best100v2/detail.nhn?catId=50000004"
식품 = "https://search.shopping.naver.com/best100v2/detail.nhn?catId=50000006"
스포츠_레저 = "https://search.shopping.naver.com/best100v2/detail.nhn?catId=50000007"
출산_육아 = "https://search.shopping.naver.com/best100v2/detail.nhn?catId=50000005"
생활_건강 = "https://search.shopping.naver.com/best100v2/detail.nhn?catId=50000008"
# 링크 리스트
category = ['패션의류', '패션잡화', '화장품_미용', '디지털_가전', '가구_인테리어', 
'식품','스포츠_레저', '출산_육아', '생활_건강']
# 네이버 쇼핑 페이지 열기 
## driver1.
driver = webdriver.Chrome()
driver.get(가구_인테리어)
serchrank = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]/div[1]/div/a[2]')
driver.execute_script("arguments[0].click();", serchrank)
# 잠깐 대기
time.sleep(2)
# 크롤링 할 부분 선택(상품검색순위)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
rank = soup.find_all("span", {"class":"txt"}) 

# 크롤링 데이터 리스트화하기
items = []
for item in rank:
    temp = []
    temp.append(item.get_text().strip())
    items.append(temp)
print(items)

# 크롤링 데이터 csv담기
import csv  
with open('./아이템.csv', 'w+',encoding='utf-8', newline='') as f:
        makewrite=csv.writer(f)

        for item in items:
            makewrite.writerow(item)


## driver1.
# 오너클랜 열고 검색하기
driver.get("https://ownerclan.com/")

for item in items:
    elem = driver.find_element_by_name("topSearchKeyword")
    elem.clear()
    elem.send_keys(item)
    elem.send_keys(Keys.RETURN)

    time.sleep(5)
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    pdname = soup.select("ul > li > p.pro_title")
    pdcost = soup.select("ul > li > div.pro_price")
    pddelcost = soup.select("ul > li > div.pro_delivery")
    pdcode = soup.select("ul > li > div.pro_code")
    pdinfo = ['\n', [(item), "상품명", "가격", "배송비", "상품코드"]]
    count = 1
    for name, cost, delcost, code in zip(pdname, pdcost, pddelcost, pdcode):
        pdinfo.append([str(count),name.text,cost.text,delcost.text,code.text])
        count = count + 1
    print(pdinfo)

    import csv  
    with open('./상품정보(오너클랜).csv', 'a',encoding='utf-8', newline='') as f:
        makewrite=csv.writer(f)

        for info in pdinfo:
            makewrite.writerow(info)
 
    

    time.sleep(2)


driver.close()
 



