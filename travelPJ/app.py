from flask import Flask, send_from_directory, render_template
# print(Flask.__version__)

app = Flask(__name__, template_folder='resources/templates', static_folder='resources/static')

# 홈 화면
@app.route('/')
def home():
    return render_template('main.html')

# favicon 파일을 정적 폴더에서 제공하도록 설정
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('resources/static/imgs', 'mapLogo.ico')

if __name__ == '__main__':
    app.run(debug=True)