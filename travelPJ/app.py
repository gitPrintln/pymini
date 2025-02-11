from flask import Flask, send_from_directory, render_template
# print(Flask.__version__)
from flask import request, redirect, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

app = Flask(__name__, template_folder='resources/templates', static_folder='resources/static')

# 홈 화면
@app.route('/')
def home():
    return render_template('main.html')

# logo 이미지 불러오기 (favicon 파일을 정적 폴더에서 제공하도록 설정)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('resources/static/imgs', 'mapLogo.ico')

# 홈 화면 search 기능
@app.route('/search', methods=['post'])
def mainSearch():
    data = request.get_json()
    selection = data.get('selection')
    query = data.get('query')
    print("query 값:", query)  # 터미널에 출력
    print("query 타입:", type(query))  # 타입 확인
    
    # 검색 데이터가 있으면
    if query:
        search_url = "https://travel.naver.com/domestic"
        naverSearch(search_url, selection, query)  # 검색 결과로 리다이렉트
        return jsonify({"message": "success"})
    else:
        return jsonify({"message": "fail"})
    
# 검색 과정(selenium, webdriver)
def naverSearch(search_url, selection, query):
    
    # 네이버 여행지 사이트로 이동
    browser = webdriver.Chrome() # 크롬창 띄우기
    browser.maximize_window() # 창 최대화
    browser.get(search_url) # 네이버 여행지
    time.sleep(1)  # 페이지 로딩 대기
    
    from selenium.webdriver.common.action_chains import ActionChains
    # 클래스명으로 검색 버튼 요소 찾기(같은게 두 개 있으므로 두번째꺼를 찾기위해 XPATH 사용)
    searchButton = browser.find_element(By.XPATH, "(//a[@class='header_search__4UCHI'])[2]")
    searchButton.click()
    
    time.sleep(1)  # 페이지 로딩 대기
    
    # 국내 여행/해외 여행 클릭
    if selection == 'overseas':
        locationSelecetBtn = browser.find_element(By.XPATH, "(//a[@class='searchbox_home_tab__RNL7F'])[2]")
        locationSelecetBtn.click()
        
    
    # 검색창 요소 찾아서 입력 후 리스트 출력
    searchInput = browser.find_element(By.CLASS_NAME, "searchInput_input__oXdGi")
    searchInput.send_keys(query)
    
    time.sleep(1)  # 페이지 로딩 대기
    
    # 리스트 요소들을 찾고 span이 query랑 같은 값이면 클릭
    listSpanElements = browser.find_elements(By.CLASS_NAME, "searchbox_home_subject__8vLI5")
    
    # 첫 번째 값이 찾는 값과 완전 같을 경우 클릭
    firstText = listSpanElements[0].text.strip()
    if firstText == query:
        listSpanElements[0].click()
    """     
    # 그게 아니라면 유사한 값이 있다는 것이기 때문에    
    for spanElement in listSpanElements[1:]:
        text = spanElement.text.strip()
        if text == query:
            spanElement.click()
            break """
            

    
    
    
    
    
    

 
if __name__ == '__main__':
    app.run(debug=True)