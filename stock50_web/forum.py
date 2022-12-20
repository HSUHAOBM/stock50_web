from flask import Blueprint, request, session, redirect, render_template, Response
from custom_models import DB_Use_message, DB_Get_stock50_everydaydata
import json

forum_blueprint = Blueprint('app_forum', __name__)
# ---Web----
# 討論區web
@forum_blueprint.route("/forum")
def web_forum():
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        stock_datas = DB_Get_stock50_everydaydata.loadstock50dataname()
        return_stock_data = []
        for i in range(len(stock_datas[0])):
            print(stock_datas[0][i])
            return_stock_data.append(stock_datas[1][i] + '－' + stock_datas[0][i])
        return render_template("forum.html",stock_data=return_stock_data)
    else:
        return redirect("/member_sigin")

# ---api----
# 預測留言新增api
@forum_blueprint.route("/api/message_predict_add", methods=["POST", "GET","DELETE"])
def message_predict_add():
    id = session.get('id')
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    member_src = session.get('member_src')
    member_level = session.get('level')

    if member_email and member_name:
        # print("登入中")
        if request.method == "POST":#留言新增
            add_member_predict_message_data = request.get_json()
            if not add_member_predict_message_data["predict_message"].strip():
                return {"error": True, "message": "檢查輸入是否為空白!"}
            elif len(add_member_predict_message_data["predict_message"]) > 200:
                return {"error": True, "message": "留言字數超過 200"}
            else:
                stock_id = add_member_predict_message_data["predict_stock"].split("－")[0]
                stock_name = add_member_predict_message_data["predict_stock"].split("－")[1]

                if(add_member_predict_message_data["predict_trend"]=="漲"):
                    predict_trend = "1"
                if(add_member_predict_message_data["predict_trend"]=="跌"):
                    predict_trend = "-1"
                if(add_member_predict_message_data["predict_trend"]=="持平"):
                    predict_trend = "0"
                message_predict_add_return = DB_Use_message.message_predict_add(id,stock_id,stock_name,predict_trend,add_member_predict_message_data["predict_message"])
                return message_predict_add_return

        if request.method == "DELETE" and member_level=="1":#留言刪除
            delete_member_predict_message_data = request.get_json()
            # print(delete_member_predict_message_data["message_id"])
            message_predict_delete_return = DB_Use_message.message_predict_delete(id,delete_member_predict_message_data["message_id"],delete_member_predict_message_data["member_user_id"])
            return message_predict_delete_return
        else:
            return {"error": True, "message": "沒有權限"}
    else:
        return {"error": True, "message": "未登入"}

# 預測留言 回復的 處理
@forum_blueprint.route("/api/message_predict_reply_add", methods=["POST", "GET","DELETE"])
def message_predict_reply_add():
    id = session.get('id')
    member_email = session.get('member_email')
    member_name = session.get('member_name')

    if member_email and member_name:
        if request.method == "POST":#留言新增
            message_predict_reply_add_data = request.get_json()
            # print(message_predict_reply_add_data)
            if not message_predict_reply_add_data["message_reply_text"].strip():
                return {"error": True, "message": "檢查輸入是否為空白!"}
            elif len(message_predict_reply_add_data["message_reply_text"]) > 50:
                return {"error": True, "message": "留言字數超過 50"}
            else:
                message_predict_reply_add_return = DB_Use_message.message_predict_add_reply(message_predict_reply_add_data["message_mid"],id,message_predict_reply_add_data["message_reply_text"])
                return message_predict_reply_add_return
    else:
        return {"error": True, "message": "未登入"}

# /api/message_predict_load?user_name=?&data_keyword=?&data_number=?&data_status=?
# 預測留言讀取api
@forum_blueprint.route("/api/message_predict_load", methods=["POST","GET"])
def message_predict_load():

    member_id = request.args.get("id", None)
    data_keyword = request.args.get("data_keyword", None)
    data_number = request.args.get("data_number", 0)
    data_status = request.args.get("data_status", None)

    id = session.get('id')

    data = DB_Use_message.message_predict_load(id,member_id,data_keyword,data_number,data_status)
    return Response(json.dumps({"ok": True,"data": data}, sort_keys = False), mimetype='application/json')

# 按讚
@forum_blueprint.route("/api/message_predict_like", methods=["POST", "GET"])
def message_predict_like():
    id = session.get('id')

    member_email = session.get('member_email')
    member_name = session.get('member_name')
    # print(member_name,member_email)

    if member_email and member_name:
        message_predict_like_data = request.get_json()
        if(message_predict_like_data['status'] == "like"):
            message_predict_like_return=DB_Use_message.message_predict_like(message_predict_like_data['message_mid_like'],id)
            return message_predict_like_return

        if(message_predict_like_data['status'] == "unlike"):
            message_predict_like_return = DB_Use_message.message_predict_unlike(message_predict_like_data['message_mid_like'],id)
            return message_predict_like_return

    else:
        return {"error": True}

