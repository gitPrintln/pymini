from flask import Blueprint, render_template, request
from .recommender import recommend_by_input

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]
        purpose, recommendations = recommend_by_input(user_input)
        return render_template("result.html", purpose=purpose, recipes=recommendations)
    return render_template("index.html")