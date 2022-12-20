from flask import *
from flask_cors import CORS
import os
from werkzeug.exceptions import HTTPException
import json

from member import member_blueprint
from forum import forum_blueprint
from rank import rank_blueprint
from stock_info import stock_info_blueprint

app = Flask(
    __name__,
    static_folder = "static",
    static_url_path = "/")

CORS(app)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = app.config["SECRET_KEY"] = os.urandom(24)

app.register_blueprint(member_blueprint)
app.register_blueprint(forum_blueprint)
app.register_blueprint(rank_blueprint)

# page
# 首頁
@app.route("/")
def index():
    return render_template("index.html")

# 關於本站
@app.route("/about_us")
def about_us_web():
    return render_template("about_web.html")

@app.errorhandler(Exception)
def handle_exception(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return Response(json.dumps(
        {"error": True, "code": code, "error_message": str(e)}, sort_keys=False), mimetype='application/json'), code

# app.run(host="0.0.0.0", port=5000)
# app.run(port=5000, debug=True)

