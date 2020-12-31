# pip install selenium
# pip install beautifulsoup4

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

fp = open("1.txt", 'r', encoding="utf-8")
text = fp.read()
fp.close()


ready_list = []
while (len(text) > 500) :
    temp_str = text[:500]
    last_space = temp_str.rfind(' ') # 500이하 글자에서 공백을 찾는다
    temp_str = text[0:last_space]
    ready_list.append(temp_str) 

    text = text[last_space:] # 검사한 글자 나머지 넣어서 범위 재조정

ready_list.append(text) # 자르고 난 뒤 500이하 글자 추가


dv = webdriver.Chrome()
dv.get("http://www.naver.com")

elem = dv.find_element_by_name("query")
elem.send_keys("맞춤법 검사기")
elem.send_keys(Keys.RETURN)


time.sleep(2)
textarea = dv.find_element_by_class_name("txt_gray")

new_str = ''
for ready in ready_list:
    textarea.send_keys(Keys.CONTROL, "a")
    textarea.send_keys(ready)

    elem = dv.find_element_by_class_name("btn_check")
    elem.click()

    time.sleep(1)

    soup = BeautifulSoup(dv.page_source, 'html.parser')
    st = soup.select("p._result_text.stand_txt")[0].text
    new_str += st.replace('. ', '.\n') # 끝나는 부분에 줄바꿈 추가 보기 좋게

fp = open("result.txt", 'w', encoding='utf-8')
fp.write(new_str)
fp.close()

