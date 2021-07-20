let login_member_email = "";
let login_member_name = "";
let login_member_img_src = "";

let google_account_use = false;



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
        // console.log(login_member_email, login_member_name)
        if (result.data != null) {
            logoin();
            document.querySelector('.member_name').textContent = "你好，" + login_member_name + "。"
            if (document.querySelector('.member_main_member_databydb.predict')) {
                member_predict_load_message()
            }
        }

    })
}
//成功 登入
function logoin() {
    head_right_login.style.display = "flex";
    head_right_logout.style.display = "none";

    // if (document.querySelector('.member_main_member_img_change')) {
    //     document.querySelector('.member_main_member_img_change').style.display = "flex";
    // }

    // if (document.querySelector('.member_modify_btn>button')) {
    //     document.querySelector('.member_modify_btn>button').style.display = "flex";
    // }
    // if (document.querySelector('.follow_btn')) {
    //     document.querySelector('.follow_btn').style.display = "none";
    // }
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
            // alert("成功登出")
            window.location.reload();
            head_member_name.textContent = ""
            head_right_login.style.display = "none";
            head_right_logout.style.display = "flex";
        }
    })
}
checklogstate();


// 目前登入的會員詳細資料讀取

function load_member_data() {
    fetch("/api/member_get_data", {
        method: 'GET'
    }).then(function(res) {
        return res.json();
    }).then(function(result) {
        login_member_img_src = result.picturesrc;
        // console.log(result);
        // 首頁上方
        if (document.querySelector('.head_welcomebox_right')) {
            document.querySelector('.head_welcomebox_right.btn7').addEventListener('click', function() {
                location.href = '/member?name=' + login_member_name
            });
        }
        // 討論區
        if (document.querySelector('.main_right_memberdata')) {
            document.querySelector('.main_right_memberdata.name').textContent = result.name;
            document.querySelector('.main_right_memberdata>img').src = result.picturesrc;

        }
        // if (document.querySelector('.member_main_member')) {
        //     document.querySelector('.member_main_member_img>img').src = result.picturesrc;
        //     document.querySelector('.member_main_member_data_.name').textContent = result.name;
        //     document.querySelector('.member_main_member_data_.interests.text').textContent = result.interests;
        //     document.querySelector('.member_main_member_data_.introduction.text').textContent = result.introduction;
        // }
        // 修改資料的讀取
        // if (document.querySelector('.member_modify_data')) {
        //     member_data_modifybox_load(result)
        // }
        // 網頁基本資料的讀取
        // if (document.querySelector('.member_main_member_databydb_memberdata_box')) {
        //     document.querySelector('.member_main_member_databydb_memberdata.text.name').textContent = result.name;
        //     document.querySelector('.member_main_member_databydb_memberdata.text.gender').textContent = result.gender;
        //     document.querySelector('.member_main_member_databydb_memberdata.text.date').textContent = result.registertime;
        //     document.querySelector('.member_main_member_databydb_memberdata.text.birthday').textContent = result.birthday;
        //     document.querySelector('.member_main_member_databydb_memberdata.text.address').textContent = result.address;
        //     document.querySelector('.member_main_member_databydb_memberdata.text.interest').textContent = result.interests;
        //     document.querySelector('.member_main_member_databydb_memberdata.text.introduction').textContent = result.introduction;

        // }
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