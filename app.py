from flask import *
from requests.api import get

from flask_cors import CORS
from custom_models import DB_Use_memberdata,up_data_to_s3,DB_Use_message,DB_Use_load_rank_data,DB_Use_load_stock_data,Get_stock_news,DB_search_data
app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/")
CORS(app)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = 'laowangaigebi'  

# page
# 首頁
@app.route("/")
def index():
    return render_template("base.html")

#/member?name=?
# 會員中心
@app.route("/member")
def web_member():
    web_user_name = request.args.get("name", None)

    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        return render_template("member_index.html")
    else:
        return redirect("/member_sigin")

@app.route("/member_data")
def web_member_data():
    web_user_name = request.args.get("name", None)


    member_email = session.get('member_email')
    member_name = session.get('member_name')
    # print(member_name)
    if member_email and member_name:
        return render_template("member_data.html")
    else:
        return redirect("/")  
@app.route("/member_rank")
def web_member_rank():    
    web_user_name = request.args.get("name", None)
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        return render_template("member_rank.html")
    else:
        return redirect("/")  
        
@app.route("/member_private")
def web_member_fans():
    web_user_name = request.args.get("name", None)

    member_name = session.get('member_name')
    if member_name==web_user_name:
        return render_template("member_private_message.html")
    else:
        return redirect("/")                    

#討論區web
@app.route("/forum")
def web_forum():
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        return render_template("forum.html")
    else:
        return redirect("/member_sigin")  
# 會員註冊web
@app.route("/member_register")
def web_member_register():
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        return redirect("/member")
    else:
        return render_template("member_register.html")
# 會員登入web
@app.route("/member_sigin")
def web_member_sigin():    
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        return redirect("/member")
    else:
        return render_template("member_sigin.html")

#各股資訊頁
@app.route("/stock_info")
def stock_info_web():
    stock_id_key = request.args.get("stock_id", None)
    print(stock_id_key)


    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        return render_template("stock_info.html")
    else:
        return redirect("/member_sigin")

#排行榜頁
@app.route("/rank")
def rank_web():
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        return render_template("rank.html")
    else:
        return redirect("/member_sigin")

@app.route("/about_us")
def about_us_web():
    return render_template("about_web.html")


#會員系統API
@app.route("/api/member", methods=["POST", "GET", "PATCH", "DELETE"])
def member():
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        print("登入中")
        if request.method == "GET":
            print("檢查登入狀況")
            return {"data": {
                "name": member_name,
                "email": member_email}}
        #登出
        if request.method == "DELETE":
            print("登出")
            session.clear()            
            return {"ok": True}
    else:
        member_data = request.get_json()
        if member_data != None:
            member_email = member_data["member_email"]
            member_password= member_data["member_password"]
            
            
            #使用地三方登入
            if(member_data.get('member_status') !=None):
                print("#使用地三方登入")
                member_name= member_data["member_name"]
                member_src= member_data["member_src"]

                # print(member_data["member_status"])
                thirdarea_return=DB_Use_memberdata.member_registered_thirdarea(member_email,member_password,member_name,member_src)
                # print(thirdarea_return['ok'])
                if(thirdarea_return['ok']):
                    session['member_email'] = thirdarea_return.get('member_email')
                    session['member_name'] = thirdarea_return.get('member_name')
                    # print("session", session)
                    return {"ok":True,"member_name":thirdarea_return.get('member_name')}

            #註冊
            if(member_data.get('member_name') != None and request.method == "POST" and member_data.get('member_status') ==None):
                # print("註冊")
                member_name= member_data["member_name"]
                # 檢查輸入是否為空白
                if not member_email.strip() or not member_password.strip() or not member_name.strip():
                    return {"error": True, "message": "檢查輸入是否為空白!"}
                elif (len(member_name)>10 or len(member_password)<6 or len(member_password)>12):
                    return {"error": True, "message": "輸入字元數不符合規定"}
                else:
                    # print(member_data,member_email,member_password,member_name)
                    returnstate=DB_Use_memberdata.member_registered(member_email,member_password,member_name)
                    return returnstate
            #登入
            if(member_data.get('member_name') == None and request.method == "PATCH" and member_data.get('member_status') ==None):
                    # 檢查輸入是否為空白
                if not member_email.strip() or not member_password.strip():
                    return {"error": True, "message": "檢查輸入是否為空白!"}
                else:
                    returnstate = DB_Use_memberdata.member_signin(member_email, member_password,request.remote_addr)
                    if(returnstate.get('ok')):
                        session['member_email'] = member_email
                        session['member_name'] = returnstate.get('member_name')
                        print("session", session)
                    return returnstate
        else:
            return {"data": None}


#/api/member_get_data?user_name=?
#會員資料處理API
@app.route("/api/member_get_data", methods=["POST", "GET"])
def member_get_data():    
    member_email = session.get('member_email')
    member_name = session.get('member_name')

    user_name = request.args.get("user_name", member_name)

    if member_email and member_name:
        # print("登入中")

        if request.method == "GET":#會員詳細資料讀取
            member_load_data_return=DB_Use_memberdata.load_member_data(user_name,member_name)
            # print(member_load_data_return)
            return member_load_data_return

        if request.method == "POST":#會員詳細資料修改
            modify_member_web_data = request.get_json()

            # print(len(modify_member_web_data["name"]))
            # print(len(modify_member_web_data["introduction"]))
            # print(len(modify_member_web_data["interests"]))
            if not modify_member_web_data["name"].strip() or not modify_member_web_data["introduction"].strip() or not modify_member_web_data["interests"].strip():
                return {"error": True, "message": "檢查輸入是否為空白!"}

            elif (len(modify_member_web_data["name"])>10 or len(modify_member_web_data["introduction"])>24 or len(modify_member_web_data["interests"])>24):
                return {"error": True, "message": "興趣、自介，請在24字以內"}
            else:
                member_modify_data_return=DB_Use_memberdata.modify_member_data (member_email,member_name,modify_member_web_data["name"],modify_member_web_data["gender"],modify_member_web_data["address"],modify_member_web_data["birthday"],modify_member_web_data["introduction"],modify_member_web_data["interests"])   
                # print("member_modify_data_return",member_modify_data_return)
                if ("modify_name" in member_modify_data_return):
                    session['member_name']=modify_member_web_data["name"]
                    # print ("session_____________",session)
                return member_modify_data_return
    else:
        return {"data": None}

#會員圖像修改api
@app.route("/api/member_modify_imgsrc", methods=["POST","GET"])
def member_modify_imgsrc():    
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        if request.method == "POST":
            # print("request",request.files)
            file = request.files['member_img_modify'] #檔案            
            # 取得圖片網址位置
            s3_img_src=up_data_to_s3.upload_file_to_s3_main(file,member_name)
            # print("file",file)   
            # print("上傳的檔案名稱",file.filename)
            # print("圖片連結網址",s3_img_src)
            member_modify_imgsrc_retrun=DB_Use_memberdata.modify_member_picturesrc(member_email,member_name,s3_img_src)
            return member_modify_imgsrc_retrun
    else:
        return {"data": None}

#預測留言新增api
@app.route("/api/message_predict_add", methods=["POST", "GET"])
def message_predict_add():
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        print("登入中")  
        if request.method == "POST":#留言新增
            add_member_predict_message_data = request.get_json()
            # print("TEST",add_member_predict_message_data["predict_message"])

            if not add_member_predict_message_data["predict_message"].strip():
                return {"error": True, "message": "檢查輸入是否為空白!"}
            elif len(add_member_predict_message_data["predict_message"])>200:
                return {"error": True, "message": "留言字數超過 200"}
            else:
                # print("TEST",add_member_predict_message_data["predict_message"])

                stock_id=add_member_predict_message_data["predict_stock"].split("－")[0]
                stock_name=add_member_predict_message_data["predict_stock"].split("－")[1]

                if(add_member_predict_message_data["predict_trend"]=="漲"):
                    predict_trend="1"
                if(add_member_predict_message_data["predict_trend"]=="跌"):
                    predict_trend="-1"            
                if(add_member_predict_message_data["predict_trend"]=="持平"):
                    predict_trend="0"

                message_predict_add_return=DB_Use_message.message_predict_add(add_member_predict_message_data["login_member_email"],add_member_predict_message_data["login_member_name"],add_member_predict_message_data["login_member_img_src"],stock_id,stock_name,predict_trend,add_member_predict_message_data["predict_message"])


                return message_predict_add_return

    else:
        return {"error": True, "message": "未登入"}

 #預測留言 回復的 新增
@app.route("/api/message_predict_reply_add", methods=["POST", "GET"])
def message_predict_reply_add():
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        print("登入中")  
        if request.method == "POST":#留言新增
            message_predict_reply_add_data = request.get_json()
            # print(message_predict_reply_add_data)
            if not message_predict_reply_add_data["message_reply_text"].strip():
                return {"error": True, "message": "檢查輸入是否為空白!"}
            elif len(message_predict_reply_add_data["message_reply_text"])>50:
                return {"error": True, "message": "留言字數超過 50"}
            else:
                message_predict_reply_add_return=DB_Use_message.message_predict_add_reply(message_predict_reply_add_data["message_mid"],message_predict_reply_add_data["login_member_email"],message_predict_reply_add_data["login_member_name"],message_predict_reply_add_data["login_member_img_src"],message_predict_reply_add_data["message_reply_text"])


                return message_predict_reply_add_return
            

    else:
        return {"error": True, "message": "未登入"}      


#/api/message_predict_load?user_name=?&data_keyword=?&data_number=?&data_status=?
#預測留言讀取api
@app.route("/api/message_predict_load", methods=["POST","GET"])
def message_predict_load():
    user_name = request.args.get("user_name", None)
    data_keyword = request.args.get("data_keyword", None)
    data_number = request.args.get("data_number", 0)
    data_status = request.args.get("data_status", None)
    # print("user_name:",user_name,"data_keyword:",data_keyword,"data_number",data_number,"data_status",data_status)
    member_name = session.get('member_name')
    # print("member_name",member_name)
    data=DB_Use_message.message_predict_load(member_name,user_name,data_keyword,data_number,data_status)
    return Response(json.dumps({"ok": True,"data": data}, sort_keys=False), mimetype='application/json')

#按讚api
@app.route("/api/message_predict_like", methods=["POST", "GET"])
def message_predict_like():
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    # print(member_name,member_email)

    if member_email and member_name:
        message_predict_like_data = request.get_json()
        # print(message_predict_like_data['status'],message_predict_like_data['login_member_name'],message_predict_like_data['login_member_email'],message_predict_like_data['message_mid_like'])
        if(message_predict_like_data['status']=="like"):
            message_predict_like_return=DB_Use_message.message_predict_like(message_predict_like_data['message_member'],message_predict_like_data['message_mid_like'],message_predict_like_data['login_member_name'])
            return message_predict_like_return
        if(message_predict_like_data['status']=="unlike"):
            message_predict_like_return=DB_Use_message.message_predict_unlike(message_predict_like_data['message_mid_like'],message_predict_like_data['login_member_name'])
            return message_predict_like_return
        # if(message_predict_like_data['status']=="check"):
        #     message_predict_like_return=DB_Use_message.message_predict_unlike(message_predict_like_data['message_mid_like'],message_predict_like_data['login_member_name'])
        #     return message_predict_like_return
    else:
        return {"error": True}
    
#取得股票訊息 /api/getstock_info?stock_id=?
@app.route("/api/getstock_info", methods=["POST","GET"])
def getstock_info_data():

    stock_id = request.args.get("stock_id", None)
    stock_load_data=DB_Use_load_stock_data.load_stock_data(stock_id)
    return Response(json.dumps({"ok": True,"data": stock_load_data}, sort_keys=False), mimetype='application/json')
#取得新聞
@app.route("/api/getstock_new", methods=["POST","GET"])
def getstock_info_news():

    stock_name = request.args.get("stock_name", "台灣50")
    Get_stock_news_return=Get_stock_news.get_news_money(stock_name)
    return Response(json.dumps({"ok": True,"data": Get_stock_news_return}, sort_keys=False), mimetype='application/json')


#/api/message_predict_rank?user_name=?&stock_id=?&data_number=?&data_status=?
#預測成績讀取api
@app.route("/api/message_predict_rank", methods=["POST","GET"])
def message_predict_rank_load():
    user_name = request.args.get("user_name", None)
    stock_id = request.args.get("stock_id", None)
    data_number = request.args.get("data_number", 0)
    data_status = request.args.get("data_status", None)

    message_predict_rank_load_data=DB_Use_load_rank_data.message_predict_rank_load(user_name,stock_id,data_number,data_status)
    return Response(json.dumps({"ok": True,"data": message_predict_rank_load_data}, sort_keys=False), mimetype='application/json')
    
#私人訊息api
@app.route("/api/private_message_sent", methods=["POST", "GET"])
def private_message_sent():
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        print("登入中")  
        if request.method == "POST":#新增
            private_message_data = request.get_json()
            if not private_message_data["message_sent_text"].strip():
                return {"error": True, "message": "檢查輸入是否為空白!"}
            elif len(private_message_data["message_sent_text"])>100:
                return {"error": True, "message": "字數超過 100"}
            else:
                private_message_add_return=DB_Use_message.private_message_add(private_message_data['login_user_name'],private_message_data['login_user_src'],private_message_data['message_sent_text'],private_message_data['message_sent'])
                return private_message_add_return
        if request.method == "GET":
            print(member_name)
            private_message_load_return=DB_Use_message.private_message_load(member_name)
            return Response(json.dumps({"ok": True,"data": private_message_load_return}, sort_keys=False), mimetype='application/json')

    else:
        return {"error": True, "message": "未登入"}


#資料尋找api
@app.route("/api/search_data", methods=["POST", "GET"])
def search_data():
    member_email = session.get('member_email')
    member_name = session.get('member_name')
    if member_email and member_name:
        print("登入中")  
        if request.method == "POST":#留言新增
            search_data = request.get_json()
            search_data_keyword=search_data['keyword']
            if not search_data_keyword.strip():
                return {"error": True, "message": "檢查輸入是否為空白!"}
            else:
                serch_return=DB_search_data.search_keyword_data(search_data_keyword)
                return  {"ok": True, "serch_return": serch_return}      
            

    else:
        return {"loging_error": True, "message": "未登入"}      




@app.errorhandler(400)
def page_400(error):
    return Response(json.dumps({"error": True, "message": "建立錯誤"}, sort_keys=False), mimetype='application/json'), 400
@app.errorhandler(500)
def page_500(error):
    return Response(json.dumps({"error": True, "message": "伺服器內部錯誤"}, sort_keys=False), mimetype='application/json'), 500





# @app.route("/test")
# def test():
#     return render_template("testt.html")
app.run(host="0.0.0.0", port=5000)
# app.run(port=5000, debug=True)

