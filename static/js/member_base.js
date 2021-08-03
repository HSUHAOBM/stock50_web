let url = location.href;
url = url.split("name=")
let web_name = url[url.length - 1]
    // console.log(web_name)


function load_member_data() {
    fetch("api/member_get_data?user_name=" + web_name, {
        method: 'GET'
    }).then(function(res) {
        return res.json();
    }).then(function(result) {
        login_member_img_src = result.picturesrc;
        // console.log(result);

        if (result.error) {
            location.href = '/'
        }
        //基本資料讀取
        if (document.querySelector('.member_main_member')) {
            document.querySelector('.member_main_member_img>img').src = result.picturesrc;
            document.querySelector('.member_main_member_data_.name').textContent = result.name;
            document.querySelector('.member_main_member_data_.interests.text').textContent = result.interests;
            document.querySelector('.member_main_member_data_.introduction.text').textContent = result.introduction;
            document.querySelector('.member_main_member_data_.good.text').textContent = result.like_total_number + "個";

            if (result.rank_total.nodata) {
                document.querySelector('.member_main_member_data_.rate.text1').textContent = "目前還沒有預測的資料";
            } else {
                document.querySelector('.member_main_member_data_.rate.text1').textContent = "成功：" + result.rank_total.win + "次、失敗：" + result.rank_total.fail + "次";
                document.querySelector('.member_main_member_data_.rate.text2').textContent = "預測：" + result.rank_total.total + "次， 勝率 " + result.rank_total.rate + " % ";
            }
            document.querySelector('.member_main_member_data').style.display = "flex";
            document.querySelector('.base_load_gif_member_basedata').style.display = "none";

        }

        // 標題連結處理
        if (document.querySelector('.member_main_head')) {
            document.querySelector('.member_main_head_btn1').addEventListener('click', function() {
                location.href = '/member?name=' + web_name
            });
            document.querySelector('.member_main_head_btn2').addEventListener('click', function() {
                location.href = '/member_data?name=' + web_name
            });
            document.querySelector('.member_main_head_btn3').addEventListener('click', function() {
                location.href = '/member_rank?name=' + web_name
            });
            document.querySelector('.member_main_head_btn4').addEventListener('click', function() {
                location.href = '/member_private?name=' + web_name
            });

        }


        // 修改資料的讀取
        if (document.querySelector('.member_modify_data')) {
            member_data_modifybox_load(result)
        }
        // 網頁基本資料的讀取
        if (document.querySelector('.member_main_member_databydb_memberdata_box')) {
            // document.querySelector('.member_main_member_databydb_memberdata.text.name').textContent = result.name;
            document.querySelector('.member_main_member_databydb_memberdata.text.gender').textContent = result.gender;
            document.querySelector('.member_main_member_databydb_memberdata.text.date').textContent = result.registertime;
            document.querySelector('.member_main_member_databydb_memberdata.text.birthday').textContent = result.birthday;
            document.querySelector('.member_main_member_databydb_memberdata.text.address').textContent = result.address;
            // document.querySelector('.member_main_member_databydb_memberdata.text.interest').textContent = result.interests;
            // document.querySelector('.member_main_member_databydb_memberdata.text.introduction').textContent = result.introduction;
            document.querySelector('.base_load_gif_member_data').style.display = "none";


        }


        if (web_name == encodeURIComponent(result.login_member_name)) {
            if (document.querySelector('.member_main_member_img_change')) {
                document.querySelector('.member_main_member_img_change').style.display = "flex";

            }
            if (document.querySelector('.member_modify_btn>button')) {
                document.querySelector('.member_modify_btn>button').style.display = "flex";
            }
            if (document.querySelector('.follow_btn')) {
                document.querySelector('.follow_btn').style.display = "none";
            }
            if (document.querySelector('.member_main_head_btn4')) {
                document.querySelector('.member_main_head_btn4').style.display = "flex";
            }
        } else {
            if (document.querySelector('.member_main_member_img_change')) {
                document.querySelector('.member_main_member_img_change').style.display = "none";

            }
            if (document.querySelector('.member_modify_btn>button')) {
                document.querySelector('.member_modify_btn>button').style.display = "none";
            }
            if (document.querySelector('.follow_btn')) {
                document.querySelector('.follow_btn').style.display = "flex";
            }
            if (document.querySelector('.member_main_head_btn4')) {
                document.querySelector('.member_main_head_btn4').style.display = "none";
            }
        }

    })
}


const member_img_modify = document.querySelector('#image_uploads');
member_img_modify.addEventListener('change', updata_img_to_ec2_rwd);

// 會員大頭貼修改
function updata_img_to_ec2_rwd() {

    var member_data_img_form = new FormData();
    member_data_img_form.append('member_img_modify', member_img_modify.files[0]);
    // console.log(member_data_img_form)

    fetch("/api/member_modify_imgsrc", {
        method: 'POST',
        body: member_data_img_form,
        // Other setting you need
        // 不需要設定 'Content-Type': 'multipart/form-data' ，已經用 FormData 物件作為請求內容了
    }).then(function(response) {
        return response.json();
    }).then(function(result) {

        console.log(result)
        if (result.ok) {
            window.location.reload();
        }
    })



}


// 修改會員資料表單 讀取原本資料
function member_data_modifybox_load(result) {
    if (document.querySelector('.member_modify_data_name')) {
        document.querySelector('.member_modify_data_name').value = result.name;
    }
    if (document.querySelector('.member_modify_data_address')) {
        document.querySelector('.member_modify_data_address').value = result.address;
    }
    if (document.querySelector('.member_modify_data_birthday')) {
        document.querySelector('.member_modify_data_birthday').value = result.birthday;
    }
    if (document.querySelector('.member_modify_data__title_gender_input1')) {
        // console.log(document.querySelector('.member_modify_data__title_gender_input1').value)
        if (document.querySelector('.member_modify_data__title_gender_input1').value == result.gender) {
            document.querySelector('.member_modify_data__title_gender_input1').checked = true;

        } else { document.querySelector('.member_modify_data__title_gender_input1').checked = false; }
    }
    if (document.querySelector('.member_modify_data__title_gender_input2')) {
        // console.log(document.querySelector('.member_modify_data__title_gender_input2').value)

        if (document.querySelector('.member_modify_data__title_gender_input2').value == result.gender) {
            document.querySelector('.member_modify_data__title_gender_input2').checked = true;
        } else { document.querySelector('.member_modify_data__title_gender_input2').checked = false; }
    }
    if (document.querySelector('.member_modify_data__title_textarea1')) {
        document.querySelector('.member_modify_data__title_textarea1').value = result.interests;
    }
    if (document.querySelector('.member_modify_data__title_textarea2')) {
        document.querySelector('.member_modify_data__title_textarea2').value = result.introduction;
    }
}




//私訊塊
function show_private_message_box() {
    // document.querySelector('.inputtextname').value = "";
    // document.querySelector('.inputtextemail').value = "";
    // document.querySelector('.inputtextpassword').value = "";
    // document.querySelector('.textpoint').textContent = "";
    document.querySelector('.private_message_box').style.display = "flex";
    document.querySelector('.private_message_box_main_top_title').textContent = "私訊給" + decodeURI(web_name);

    //灰層
    let hidebg = document.getElementById("hidebg_private");
    hidebg.style.display = "block";
    hidebg.style.height = document.body.clientHeight + "px";
}

function close_private_message_box() {
    document.querySelector('.private_message_box').style.display = "none";
    //灰層
    document.getElementById("hidebg_private").style.display = "none";
}

//字數判斷
function check_input_private_message(value) {
    // console.log(value)
    let maxLen = 100;


    if (value.length > maxLen) {
        document.querySelector('.private_message_box_text_textarea').value = value.substring(0, maxLen);
        // console.log(value)
    }
    // otherwise, update 'characters left' counter 
    else if (value.length == 0) {
        document.querySelector('.private_message_box_error_text').style.display = "none"
    } else {
        document.querySelector('.private_message_box_error_text').textContent = maxLen - value.length;
        document.querySelector('.private_message_box_error_text').style.display = "flex"
    }
}


// 傳送私人訊息會員資料
let member_private_message_form = document.getElementById('member_private_message');
member_private_message_form.addEventListener('submit', function(event) {
    var member_private_message_form_ = new FormData(member_private_message_form);
    let member_private_message_form_data = {};
    event.preventDefault();
    member_private_message_form_data = {
        "login_user_name": login_member_name,
        "login_user_src": login_member_img_src,
        "message_sent_text": member_private_message_form_.get("private_message_text"),
        "message_sent": decodeURI(web_name)
    }
    if (member_private_message_form_.get("private_message_text").length > 100) {
        document.querySelector('.private_message_box_error_text').textContent = "字數大於100，超過規定。";
    }

    fetch("/api/private_message_sent", {
        method: "POST",
        body: JSON.stringify(member_private_message_form_data),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(result) {
        // console.log(result);
        if (result.ok) {
            // location.href = '/member?name=' + member_modify_data_form_.get("member_modify_name")
            window.location.reload();

        }
        if (result.error) {
            document.querySelector('.private_message_box_error_text').textContent = result.message;
        }



    })

})




load_member_data()