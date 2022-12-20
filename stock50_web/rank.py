from flask import Blueprint, request, session, redirect, render_template, Response
from custom_models import DB_Use_load_rank_data, DB_Use_load_stock_data, Get_stock_news
import json

rank_blueprint = Blueprint('app_rank', __name__)

#排行榜頁web
@rank_blueprint.route("/rank")
def rank_web():
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        return render_template("rank.html")
    else:
        return redirect("/member_sigin")

#/api/message_predict_rank?user_name=?&stock_id=?&data_number=?&data_status=?
# 預測成績讀取
@rank_blueprint.route("/api/message_predict_rank", methods=["POST","GET"])
def message_predict_rank_load():
    member_id = request.args.get("id", None)

    stock_id = request.args.get("stock_id", None)
    data_number = request.args.get("data_number", 0)
    data_status = request.args.get("data_status", None)

    message_predict_rank_load_data = DB_Use_load_rank_data.message_predict_rank_load(member_id,stock_id,data_number,data_status)
    return Response(json.dumps({"ok": True,"data": message_predict_rank_load_data}, sort_keys=False), mimetype='application/json')

