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


        //基本資料讀取
        if (document.querySelector('.member_main_member')) {
            document.querySelector('.member_main_member_img>img').src = result.picturesrc;
            document.querySelector('.member_main_member_data_.name').textContent = result.name;
            document.querySelector('.member_main_member_data_.interests.text').textContent = result.interests;
            document.querySelector('.member_main_member_data_.introduction.text').textContent = result.introduction;
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
                location.href = '/member_fans?name=' + web_name
            });

        }


        // 修改資料的讀取
        if (document.querySelector('.member_modify_data')) {
            member_data_modifybox_load(result)
        }
        // 網頁基本資料的讀取
        if (document.querySelector('.member_main_member_databydb_memberdata_box')) {
            document.querySelector('.member_main_member_databydb_memberdata.text.name').textContent = result.name;
            document.querySelector('.member_main_member_databydb_memberdata.text.gender').textContent = result.gender;
            document.querySelector('.member_main_member_databydb_memberdata.text.date').textContent = result.registertime;
            document.querySelector('.member_main_member_databydb_memberdata.text.birthday').textContent = result.birthday;
            document.querySelector('.member_main_member_databydb_memberdata.text.address').textContent = result.address;
            document.querySelector('.member_main_member_databydb_memberdata.text.interest').textContent = result.interests;
            document.querySelector('.member_main_member_databydb_memberdata.text.introduction').textContent = result.introduction;


        }
        // console.log("login_member_name", result.login_member_name)
        // console.log("web_name", web_name)

        if (web_name == encodeURIComponent(result.login_member_name)) {
            console.log("登入人為畫面使用者")
            if (document.querySelector('.member_main_member_img_change')) {
                document.querySelector('.member_main_member_img_change').style.display = "flex";

            }
            if (document.querySelector('.member_modify_btn>button')) {
                document.querySelector('.member_modify_btn>button').style.display = "flex";
            }
            if (document.querySelector('.follow_btn')) {
                document.querySelector('.follow_btn').style.display = "none";
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
        }

    })
}
load_member_data()


const member_img_modify = document.querySelector('#image_uploads');
member_img_modify.addEventListener('change', updata_img_to_ec2_rwd);

// 會員大頭貼修改
function updata_img_to_ec2_rwd() {

    var member_data_img_form = new FormData();
    member_data_img_form.append('member_img_modify', member_img_modify.files[0]);
    console.log(member_data_img_form)

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
/*
 
<div class="member_main_member_img_change" style="display: flex;">
                    <label for="image_uploads">更換大頭貼</label>
                    <input type="file" id="image_uploads" name="image_uploads" accept=".jpg, .jpeg, .png" multiple="">
                </div>
*/

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