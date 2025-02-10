from flask import Flask, send_from_directory, render_template
# print(Flask.__version__)
from flask import request, redirect, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By

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
@app.route('/search')
def mainSearch():
    query = request.args.get('query')
    if query:
        search_url = f"https://search.naver.com/search.naver?query={query} 여행"
        return naverSearch(search_url)  # 검색 결과로 리다이렉트
    return naverSearch(search_url)
    
# 검색 과정(selenium, webdriver)
def naverSearch(search_url):
    # 네이버 여행지 사이트로 이동
    browser = webdriver.Chrome() # 크롬창 띄우기
    browser.maximize_window() # 창 최대화
    browser.get(search_url) # 네이버 여행지
    
    # 검색 후 검색창 비우기
    

# 검색 후 검색창 비우기
@app.route('/clearInput', methods=["post"])
def clearInput():
    return jsonify({"new_value": ""})  # 클라이언트에 빈 문자열 반환

if __name__ == '__main__':
    app.run(debug=True)