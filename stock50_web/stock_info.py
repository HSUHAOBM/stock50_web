from flask import Blueprint, request, session, redirect, render_template, Response
from custom_models import DB_Use_load_stock_data, Get_stock_news, DB_search_data
import json

stock_info_blueprint = Blueprint('app_stock_info', __name__)

# 股資訊頁
@stock_info_blueprint.route("/stock_info")
def stock_info_web():
    stock_id_key = request.args.get("stock_id", None)
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        return render_template("stock_info.html")
    else:
        return redirect("/member_sigin")

#取得股票訊息 /api/getstock_info?stock_id=?
@stock_info_blueprint.route("/api/getstock_info", methods=["POST","GET"])
def getstock_info_data():
    stock_id = request.args.get("stock_id", None)
    stock_load_data = DB_Use_load_stock_data.load_stock_data(stock_id)
    return Response(json.dumps({"ok": True,"data": stock_load_data}, sort_keys=False), mimetype='application/json')

#取得新聞
@stock_info_blueprint.route("/api/getstock_new", methods=["POST","GET"])
def getstock_info_news():
    stock_name = request.args.get("stock_name", "台灣50")
    Get_stock_news_return = Get_stock_news.get_news_money(stock_name)
    return Response(json.dumps({"ok": True,"data": Get_stock_news_return}, sort_keys=False), mimetype='application/json')


#資料尋找api
@stock_info_blueprint.route("/api/search_data", methods=["POST", "GET"])
def search_data():
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        if request.method == "POST":
            search_data = request.get_json()
            search_data_keyword = search_data['keyword']
            if not search_data_keyword.strip():
                return {"error": True, "message": "檢查輸入是否為空白!"}
            else:
                serch_return = DB_search_data.search_keyword_data(search_data_keyword)
                return  {"ok": True, "serch_return": serch_return}
    else:
        return {"loging_error": True, "message": "未登入"}
