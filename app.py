from flask import *
from requests.api import get

from flask_cors import CORS

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/")
CORS(app)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = 'laowangaigebi'  # key


# 首頁
@app.route("/")
def index():
    return render_template("test.html")

# 會員
@app.route("/member")
def web_member():
    return render_template("test.html")
# 會員註冊
@app.route("/member_register")
def web_member_register():
    return render_template("member_register.html")


@app.errorhandler(400)
def page_400(error):
    return Response(json.dumps({"error": True, "message": "建立錯誤"}, sort_keys=False), mimetype='application/json'), 400


@app.errorhandler(500)
def page_500(error):
    return Response(json.dumps({"error": True, "message": "伺服器內部錯誤"}, sort_keys=False), mimetype='application/json'), 500


# app.run(host="0.0.0.0", port=5000)
app.run(port=5000, debug=True)

