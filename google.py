from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import urllib.request
import os



search_name=input("찾고 싶은 이미지를 검색하세요: ")
txt_folder = 'C:/users/tjral/Desktop/웹크롤링'
add_folder=input("새로 만들 폴더 이름을 적으세요. (없으면 엔터): ")
max_img=int(input("원하는 이미지 저장 개수를 입력하세요: "))
pages = int((max_img-1)/100)+1 #한 페이지당 표시되는 이미지 수(100)을 참고하여 확인할 페이지 수 계산

if not os.path.isdir(txt_folder+'/'+add_folder) : # 없으면 새로 생성하는 조건문 
    os.mkdir(txt_folder+'/'+add_folder)
    print(f"{add_folder} 이름의 폴더 생성")
else:
    print("이미 생성되어있는 폴더입니다.")

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options)
driver.get("https://www.google.co.kr/imghp?hl=ko")
elem = driver.find_element(By.NAME, "q")    #특정 요소 찾기(검색어 찾기)
elem.send_keys(search_name)                 #검색어에 찾을 거 이름
elem.send_keys(Keys.RETURN)                 #엔터키 전송 코드

SCROLL_PAUSE_SEC = 1.3

# 스크롤 높이 가져옴
last_height = driver.execute_script("return document.body.scrollHeight")

#페이지 수만큼 반복
for i in range(pages):
    # 끝까지 스크롤 다운
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 1초 대기
    time.sleep(SCROLL_PAUSE_SEC)

    # 스크롤 다운 후 스크롤 높이 다시 가져옴
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element(By.CSS_SELECTOR,'.mye4qd').click()
            time.sleep(1.3)
        except:
            break
    last_height = new_height


#element는 하나, elements는 여러 개, css_selecetor로 요소 선택 
lists= driver.find_elements(By.CSS_SELECTOR, '.rg_i.Q4LuWd')
count=1

for image in lists:
    try:        
        image.click()
        time.sleep(1.5)
        url=(driver.find_element(By.CSS_SELECTOR, ".r48jcc.pT0Scc.iPVvYb").get_attribute('src')) #요소의 속성 값 가져오기
        urllib.request.urlretrieve(url, (txt_folder+'/'+add_folder+'/'+search_name+str(count)+".jpg"))
        if max_img==count:
            break
        count+=1
    except:
        pass

print(f"{count}개 이미지가 다운받아졌습니다")

driver.close()