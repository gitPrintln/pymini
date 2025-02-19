from flask import Flask, send_from_directory, render_template

app = Flask(__name__, template_folder='resources/templates', static_folder='resources/static')

# 홈 화면
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)