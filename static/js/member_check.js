let login_member_email = "";
let login_member_name = "";
let login_member_img_src = "";
let login_data_get = false
checklogstate();



let head_right_logout = document.querySelector('.head_right.logout');
let head_right_login = document.querySelector('.head_right.login');
//檢查登入狀況
function checklogstate() {
    // console.log("檢查登入狀況")
    fetch("/api/member", {
        method: 'GET'
    }).then(function(res) {
        return res.json();
    }).then(function(result) {
        // console.log(result);
        // console.log(result.data.email, result.data.name);
        login_member_email = result.data.email;
        login_member_name = result.data.name;
        login_data_get = true

        // console.log(login_member_email, login_member_name)
        if (result.data != null) {
            logoin();
            document.querySelector('.member_name').textContent = "你好，" + login_member_name + "。"
            if (document.querySelector('.member_main_member_databydb.predict')) {
                member_predict_load_message()

            }
            if (document.querySelector('.member_main_member_databydb.rank')) {

                member_predict_load_rank("rate")
                member_predict_load_rank("win")
                member_predict_load_rank("fail")
            }
        }

    })
}
//成功 登入
function logoin() {
    head_right_login.style.display = "flex";
    head_right_logout.style.display = "none";

    load_member_data()
}

//成功 登出 
function logout() {
    // alert("登出")

    signOut()
    fetch("/api/member", {
        method: 'DELETE'
    }).then(function(res) {
        return res.json();
    }).then(function(result) {
        console.log(result);
        if (result.ok) {
            location.href = '/'

            // alert("成功登出")                    

            head_member_name.textContent = ""
            head_right_login.style.display = "none";
            head_right_logout.style.display = "flex";
        }
    })
}


// 目前登入的會員詳細資料讀取

function load_member_data() {
    fetch("/api/member_get_data", {
        method: 'GET'
    }).then(function(res) {
        return res.json();
    }).then(function(result) {
        // console.log(result)
        if (result) {
            login_member_img_src = result.picturesrc;
            // 首頁上方
            if (document.querySelector('.head_welcomebox_right')) {
                document.querySelector('.head_welcomebox_right.btn7').addEventListener('click', function() {
                    location.href = '/member?name=' + login_member_name
                });
            }
            // 討論區
            if (document.querySelector('.main_right_memberdata')) {
                document.querySelector('.main_right_memberdata.name').textContent = result.name;
                document.querySelector('.main_right_memberdata.name').addEventListener('click', function() {
                    location.href = '/member?name=' + result.name
                });
                document.querySelector('.main_right_memberdata_div>img').src = result.picturesrc;
                if (result.rank_total.ok) {
                    document.querySelector('.main_right_memberdata.rate').textContent = "勝率：" + result.rank_total.rate + " %";
                    document.querySelector('.main_right_memberdata.success').textContent = "成功：" + result.rank_total.win + " 次";
                    document.querySelector('.main_right_memberdata.fail').textContent = "失敗：" + result.rank_total.fail + " 次";
                    document.querySelector('.main_right_memberdata.message').textContent = "預測：" + result.rank_total.total + " 次";
                    document.querySelector('.main_right_memberdata.like').textContent = "讚：" + result.like_total_number + " 個";

                }
                if (result.rank_total.nodata) {
                    document.querySelector('.main_right_memberdata.rate').textContent = "目前沒有預測的成績";
                    document.querySelector('.main_right_memberdata.success').textContent = "-資料於收盤後更新-";
                    document.querySelector('.main_right_memberdata.fail').style.display = "none"
                    document.querySelector('.main_right_memberdata.message').style.display = "none"
                    document.querySelector('.main_right_memberdata.like').style.display = "none"
                }
                document.querySelector('.main_right_memberdata_div').style.display = "flex";
                document.querySelector('.base_load_gif_forum_memberdata').style.display = "none";


            }
        }
    })
}



function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function() {
        console.log('User signed out.');
    });
}

function onLoad() {
    gapi.load('auth2', function() {
        gapi.auth2.init();
    });
}