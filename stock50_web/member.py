from flask import Blueprint, request, session, redirect, render_template, Response
from werkzeug.utils import secure_filename
from custom_models import DB_Use_memberdata, DB_Use_message, google_account_verify
import os
import uuid
import json

member_blueprint = Blueprint('app_member', __name__)
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']

# ---Web----
# 會員中心
@member_blueprint.route("/member")
def web_member():
    member_id = request.args.get("id", None)
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        return render_template("member_index.html")
    else:
        return redirect("/member_sigin")

@member_blueprint.route("/member_data")
def web_member_data():
    member_id = request.args.get("id", None)
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    # print(member_name)
    if member_email and member_name:
        return render_template("member_data.html")
    else:
        return redirect("/")

@member_blueprint.route("/member_rank")
def web_member_rank():
    member_id = request.args.get("id", None)
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        return render_template("member_rank.html")
    else:
        return redirect("/")

@member_blueprint.route("/member_private")
def web_member_fans():
    member_id = request.args.get("id", None)
    id = session.get('id')
    if int(id) == int(member_id):
        return render_template("member_private_message.html")
    else:
        return redirect("/")
# 會員註冊
@member_blueprint.route("/member_register")
def web_member_register():
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        return redirect("/")
    else:
        return render_template("member_register.html")

# 會員登入web
@member_blueprint.route("/member_sigin")
def web_member_sigin():
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        return redirect("/")
    else:
        return render_template("member_sigin.html")

# ---api----
# 會員系統
@member_blueprint.route("/api/member", methods=["POST", "GET", "PATCH", "DELETE"])
def member():
    id = session.get('id')
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    member_src = session.get('member_src')

    if member_email and member_name:
        if request.method == "GET":
            return {"data": {
                "login_name": member_name,
                "login_email": member_email,
                "login_imgsrc":member_src,
                "login_id":id}}
        #登出
        if request.method == "DELETE":
            session.clear()
            return {"ok": True}
    else:
        member_data = request.get_json()
        if member_data != None:
            #使用地三方登入
            if(member_data.get('member_status') !=None):

                id_token = member_data["id_token"]

                gmail_member_name,gmail_member_email,gmail_member_password,gmail_member_src=google_account_verify.google_verify_oauth2_token(id_token)

                thirdarea_return = DB_Use_memberdata.member_registered_thirdarea(gmail_member_email,gmail_member_password,gmail_member_name,gmail_member_src)
                if(thirdarea_return['ok']):
                    session.clear()
                    session['id'] = thirdarea_return.get('id')
                    session['member_email'] = thirdarea_return.get('member_email')
                    session['member_name'] = thirdarea_return.get('member_name')
                    session['member_src'] = thirdarea_return.get("member_src")
                    session['level'] = thirdarea_return.get("level")
                    # print("--------------session-----------", session)
                    return {"ok":True,"member_name":thirdarea_return.get('member_name'),"member_id":thirdarea_return.get('id')}
            else:
                member_email = member_data["member_email"]
                member_password = member_data["member_password"]
                print('123')
                #註冊
                if(member_data.get('member_name') != None and request.method == "POST" and member_data.get('member_status') ==None):
                    print("註冊")
                    member_name = member_data["member_name"]
                    # 檢查輸入是否為空白
                    if not member_email.strip() or not member_password.strip() or not member_name.strip():
                        return {"error": True, "message": "檢查輸入是否為空白!"}
                    elif (len(member_name) > 10 or len(member_password) < 6 or len(member_password) > 12):
                        return {"error": True, "message": "輸入字元數不符合規定"}
                    else:
                        returnstate = DB_Use_memberdata.member_registered(member_email,member_password,member_name)
                        return returnstate
                #登入
                if(member_data.get('member_name') == None and request.method == "PATCH" and member_data.get('member_status') ==None):
                        # 檢查輸入是否為空白
                    if not member_email.strip() or not member_password.strip():
                        return {"error": True, "message": "檢查輸入是否為空白!"}
                    else:
                        returnstate = DB_Use_memberdata.member_signin(member_email, member_password,request.remote_addr)
                        if(returnstate.get('ok')):
                            session.clear()
                            session['id']=  returnstate.get('member_id')
                            session['member_email'] = member_email
                            session['member_name'] = returnstate.get('member_name')
                            session['member_src']= returnstate.get('picturesrc')
                            session['level'] = returnstate.get("level")
                        return returnstate
        else:
            return {"data": None}

# /api/member_get_data?user_name=?
# 會員資料處理
@member_blueprint.route("/api/member_get_data", methods=["POST", "GET"])
def member_get_data():
    id = session.get('id')
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    member_id = request.args.get("id", id)

    if member_email and member_name:
        if request.method == "GET":#會員詳細資料讀取
            member_load_data_return = DB_Use_memberdata.load_member_data(member_id,member_name,id)
            # print(member_load_data_return)
            return member_load_data_return

        if request.method == "POST":#會員詳細資料修改
            modify_member_web_data = request.get_json()

            if not modify_member_web_data["name"].strip() or not modify_member_web_data["introduction"].strip() or not modify_member_web_data["interests"].strip():
                return {"error": True, "message": "檢查輸入是否為空白!"}

            elif (len(modify_member_web_data["name"])>10 or len(modify_member_web_data["introduction"])>24 or len(modify_member_web_data["interests"])>24):
                return {"error": True, "message": "興趣、自介，請在24字以內"}
            else:
                member_modify_data_return = DB_Use_memberdata.modify_member_data (id,member_email,member_name,modify_member_web_data["name"],modify_member_web_data["gender"],modify_member_web_data["address"],modify_member_web_data["birthday"],modify_member_web_data["introduction"],modify_member_web_data["interests"])
                if ("modify_name" in member_modify_data_return):
                    session['member_name'] = modify_member_web_data["name"]
                return member_modify_data_return
    else:
        return {"data": None}

# 頭貼判斷格式
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS

#會員頭貼修改api
@member_blueprint.route("/api/member_modify_imgsrc", methods=["POST","GET"])
def member_modify_imgsrc():
    id = session.get('id')
    member_email = session.get('member_email')
    member_name = session.get('member_name')

    if member_email and member_name:
        if request.method == "POST":
            try:
                file = request.files['member_img_modify'] #檔案
                if file and allowed_file(file.filename):
                    # secure_filename方法清除中文，取後綴
                    file_name_hz = secure_filename(file.filename).split('.')[-1]
                    # uuid 生成唯一名稱
                    first_name = str(uuid.uuid4())
                    # 文件名
                    file_name = first_name + '.' + file_name_hz
                    # 保存路徑
                    file_path = './static/image/member/'
                    # 檢查路徑
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)
                    file.save(os.path.join(file_path, file_name))
                    member_modify_imgsrc_retrun = DB_Use_memberdata.modify_member_picturesrc(id , './image/member/' + file_name)
                    # 移除 舊的圖
                    if os.path.exists('./static' + session['member_src'][1:]):
                        os.remove('./static' + session['member_src'][1:])
                    session['member_src'] = './image/member/' + file_name
            except Exception as e:
                print(e)
            return member_modify_imgsrc_retrun

# 私人訊息
@member_blueprint.route("/api/private_message_sent", methods=["POST", "GET"])
def private_message_sent():
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    member_src = session.get('member_src')
    id = session.get('id')

    if member_email and member_name:
        if request.method == "POST":#新增
            private_message_data = request.get_json()
            if not private_message_data["message_sent_text"].strip():
                return {"error": True, "message": "檢查輸入是否為空白!"}
            elif len(private_message_data["message_sent_text"])>100:
                return {"error": True, "message": "字數超過 100"}
            else:
                private_message_add_return = DB_Use_message.private_message_add(id,private_message_data['message_sent_text'],private_message_data['message_sent'])
                return private_message_add_return
        if request.method == "GET":
            private_message_load_return = DB_Use_message.private_message_load(id)
            return Response(json.dumps({"ok": True,"data": private_message_load_return}, sort_keys=False), mimetype='application/json')

    else:
        return {"error": True, "message": "未登入"}

# 私人聯絡管理員
@member_blueprint.route("/api/contact_message_sent", methods=["POST", "GET"])
def contact_message_sent():
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    member_src = session.get('member_src')
    id = session.get('id')

    if member_email and member_name:
        if request.method == "POST":
            contact_message_data = request.get_json()
            if not contact_message_data["message_sent_text"].strip():
                return {"error": True, "message": "檢查輸入是否為空白!"}
            elif len(contact_message_data["message_sent_text"])>500:
                return {"error": True, "message": "字數超過 500"}
            else:
                contact_message_add_return = DB_Use_message.contact_message_add(id,contact_message_data["message_sent_text"])
                return contact_message_add_return
        if request.method == "GET":
            contact_message_load_return = DB_Use_message.contact_message_load()
            return Response(json.dumps({"ok": True,"data": contact_message_load_return}, sort_keys=False), mimetype='application/json')

    else:
        return {"error": True, "message": "未登入"}

