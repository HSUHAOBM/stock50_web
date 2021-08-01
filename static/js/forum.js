let check_function_end = true;
let forum_page = 0;
let check_onload = true;

document.querySelector('.main_left_center').innerText = ""

// 預測留言根據選擇變化
function stock_select_change() {
    let stock_select_textContent = document.querySelector('.stock_select_list');
    let index = stock_select_textContent.selectedIndex
    let stock_select_out_text = stock_select_textContent.options[index].text

    document.querySelector('.member_out_stock.name').href = "stock_info?stock_id=" + stock_select_out_text.split("－")[0]

    document.querySelector('.member_out_stock.name').textContent = stock_select_out_text;
    document.querySelector('.member_out_text').style.display = "flex";
    document.querySelector('.textInput').placeholder = "分享你對 " + stock_select_out_text + " 的想法 ...";

}

function trend_radio_change(text) {
    let out_text = ""
    if (text == 1) {
        out_text = "漲"
    } else if (text == 2) {
        out_text = "跌"
    } else if (text == 3) {
        out_text = "持平"
    }
    document.querySelector('.member_out_stock.trend').textContent = " " + out_text;
    document.querySelector('.member_out_text').style.display = "flex";
    document.querySelector('.div_message_btn_img.img1').style.opacity = "0.4"
    document.querySelector('.div_message_btn_img.img2').style.opacity = "0.4"
    document.querySelector('.div_message_btn_img.img3').style.opacity = "0.4"

    document.querySelector('.div_message_btn_img.img' + text).style.opacity = "1"
    document.querySelector('.div_message_btn.bt1').style.backgroundColor = " white"
    document.querySelector('.div_message_btn.bt2').style.backgroundColor = " white"
    document.querySelector('.div_message_btn.bt3').style.backgroundColor = " white"

    document.querySelector('.div_message_btn.bt' + text).style.backgroundColor = " rgb(247 247 247)"

}
/*----------留言板字數監控---------*/

function check_input(value) {
    let maxLen = 200;
    if (value.length > maxLen) {
        document.querySelector('.textInput').value = value.substring(0, maxLen);
        // console.log(value)
    }
    // otherwise, update 'characters left' counter 
    else document.querySelector('.member_out_btn_error_text').textContent = maxLen - value.length;
}

function check_input_(value, alt) {
    // console.log(value, alt)
    let maxLen = 50;


    if (value.length > maxLen) {
        document.querySelector('.textarea_message_box_other_message_write.' + alt).value = value.substring(0, maxLen);
        // console.log(value)
    }
    // otherwise, update 'characters left' counter 
    else if (value.length == 0) {
        document.querySelector('.message_box_text_btn_error_text.' + alt).style.display = "none"
    } else {
        document.querySelector('.message_box_text_btn_error_text.' + alt).textContent = maxLen - value.length;
        document.querySelector('.message_box_text_btn_error_text.' + alt).style.display = "flex"
    }
}


/*-----------------------------*/
// 送出預測
let member_predict_data_form = document.getElementById('member_predict_data');
member_predict_data_form.addEventListener('submit', function(event) {
    if (check_function_end) {
        check_function_end = false
        var member_predict_data_form_ = new FormData(member_predict_data_form);
        let member_predict_form_data = {};
        event.preventDefault();
        predict_message = member_predict_data_form_.get("member_predict_message")
        member_predict_form_data = {
                "predict_stock": member_predict_data_form_.get("member_predict_stock"),
                "predict_trend": member_predict_data_form_.get("member_predict_trend"),
                "predict_message": predict_message,
                "login_member_name": login_member_name,
                "login_member_email": login_member_email,
                "login_member_img_src": login_member_img_src
            }
            // console.log(member_predict_form_data);
        if (predict_message.length <= 200) {
            fetch("/api/message_predict_add", {
                method: "POST",
                body: JSON.stringify(member_predict_form_data),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(function(res) {
                return res.json();
            }).then(function(result) {
                if (result.ok) {
                    console.log(result);
                    // member_predict_add_message(member_predict_data_form_.get("member_predict_stock"), member_predict_data_form_.get("member_predict_trend"), predict_message, login_member_name, login_member_img_src, result.time, result.mid)

                    window.location.reload();
                }
                if (result.error) {

                    document.querySelector('.member_out_btn_error_text').textContent = result.message;
                    check_function_end = true;
                }
            })
        } else {
            document.querySelector('.member_out_btn_error_text').textContent = "字數不得超過200字";
            check_function_end = true;

        }


    }
})

// ------------------------產生畫面-----------------

let main_left_center = document.querySelector('.main_left_center')

function member_predict_add_message(predict_stock, predict_trend, predict_message, predict_message_member_name, predict_message_member_img_src, time, time_about, message_mid, message_check_status, login_member_name_good_have, message_good_number, message_reply_number, message_reply_data) {
    let div_predict_message_box = document.createElement("div");
    div_predict_message_box.className = "predict_message_box";

    // if (main_left_center.firstChild == null) {

    //     main_left_center.appendChild(div_predict_message_box)
    // } else {

    //     main_left_center.insertBefore(div_predict_message_box, main_left_center.childNodes[0]);
    //     //父.insertBefore(加入，被加入)
    // }

    main_left_center.appendChild(div_predict_message_box)

    //<div class="predict_message_box_result"><img src=" img/fail.png " alt=" "></div>
    let div_predict_message_box_result = document.createElement("div");
    div_predict_message_box_result.className = "predict_message_box_result";
    div_predict_message_box.appendChild(div_predict_message_box_result)

    // 預測檢測後的顯示
    let imgdiv_predict_message_box_result = document.createElement("img");
    if (message_check_status == "0") {
        imgdiv_predict_message_box_result.src = ""
    }
    if (message_check_status == "1") {
        imgdiv_predict_message_box_result.src = "img/success.png"
        imgdiv_predict_message_box_result.style.opacity = "0.25";
    }
    if (message_check_status == "-1") {
        imgdiv_predict_message_box_result.src = "img/fail.png"
        imgdiv_predict_message_box_result.style.opacity = "0.25";

    }
    div_predict_message_box_result.appendChild(imgdiv_predict_message_box_result)


    let div_predict_message_box_image = document.createElement("div");
    div_predict_message_box_image.className = "predict_message_box_image";
    div_predict_message_box.appendChild(div_predict_message_box_image)

    let img_div_div_content_img = document.createElement("img");
    img_div_div_content_img.src = predict_message_member_img_src
    div_predict_message_box_image.appendChild(img_div_div_content_img)


    let div_predict_message = document.createElement("div");
    div_predict_message.className = "predict_message";
    div_predict_message_box.appendChild(div_predict_message)

    /* */
    let div_message_box_loaddata = document.createElement("div");
    div_message_box_loaddata.className = "message_box_loaddata";
    div_predict_message.appendChild(div_message_box_loaddata)

    let div_message_box_title = document.createElement("div");
    div_message_box_title.className = "message_box_title";
    div_message_box_loaddata.appendChild(div_message_box_title);

    let a_message_box_title_name = document.createElement("a");
    a_message_box_title_name.className = "message_box_title_name " + message_mid
    a_message_box_title_name.setAttribute("href", "/member?name=" + predict_message_member_name)
    a_message_box_title_name.textContent = predict_message_member_name
    div_message_box_title.appendChild(a_message_box_title_name)

    let div_message_box_predict = document.createElement("div")
    div_message_box_predict.className = "message_box_predict"
        // div_message_box_predict.textContent = "預測：" + predict_stock + "的下次開盤走勢為" + predict_trend;
    div_message_box_loaddata.appendChild(div_message_box_predict);

    let a_message_box_predict_1 = document.createElement("a")
    a_message_box_predict_1.textContent = "預測："
    div_message_box_predict.appendChild(a_message_box_predict_1);

    let a_message_box_predict_2 = document.createElement("a")
    a_message_box_predict_2.textContent = predict_stock
    a_message_box_predict_2.className = "message_box_predict_stock"
    let stock_id = predict_stock.split("－")
    a_message_box_predict_2.setAttribute("href", "stock_info?stock_id=" + stock_id[0])

    div_message_box_predict.appendChild(a_message_box_predict_2);

    let a_message_box_predict_3 = document.createElement("a")
    a_message_box_predict_3.textContent = "的下次開盤走勢為" + predict_trend;
    div_message_box_predict.appendChild(a_message_box_predict_3);




    let div_message_box_text = document.createElement("div")
    div_message_box_text.className = "message_box_text"
    div_message_box_text.textContent = predict_message;
    div_message_box_loaddata.appendChild(div_message_box_text);
    /* */

    let div_message_box_text_btn = document.createElement("div")
    div_message_box_text_btn.className = "message_box_text_btn"
    div_predict_message.appendChild(div_message_box_text_btn)

    let div_message_box_date = document.createElement("div")
    div_message_box_date.className = "message_box_date"
    div_message_box_date.textContent = time_about
    div_message_box_date.setAttribute("title", time)
    div_message_box_text_btn.appendChild(div_message_box_date)

    let div_message_box_btn = document.createElement("div")
    div_message_box_btn.className = "message_box_btn"
    div_message_box_text_btn.appendChild(div_message_box_btn)

    let div_message_box_btn_like = document.createElement("div")
    div_message_box_btn_like.className = "message_box_btn_like"
    div_message_box_btn_like.setAttribute("id", message_mid)
    div_message_box_btn_like.setAttribute("alt", message_mid)



    if (login_member_name_good_have) {
        div_message_box_btn_like.onclick = function() {
            let message_mid = this.getAttribute('alt');
            // let message_member = document.querySelector('.message_box_title_name.' + message_mid).textContent
            // console.log(message_member)
            predict_message_btn_enter_unlike(message_mid)

        }
        div_message_box_btn.appendChild(div_message_box_btn_like)

        let a_div_message_box_btn_like = document.createElement("a")
        a_div_message_box_btn_like.textContent = "讚 (" + message_good_number + ")"
        div_message_box_btn_like.appendChild(a_div_message_box_btn_like)

        let img_div_message_box_btn_like = document.createElement("img")
        img_div_message_box_btn_like.src = "img/likeA.png"
        div_message_box_btn_like.appendChild(img_div_message_box_btn_like)
    } else {


        div_message_box_btn_like.onclick = function() {
            let message_mid = this.getAttribute('alt');
            let message_member = document.querySelector('.message_box_title_name.' + message_mid).textContent
                // console.log(message_member)
            predict_message_btn_enter_like(message_mid, message_member)

        }
        div_message_box_btn.appendChild(div_message_box_btn_like)

        let a_div_message_box_btn_like = document.createElement("a")
        a_div_message_box_btn_like.textContent = "讚 (" + message_good_number + ")"
        div_message_box_btn_like.appendChild(a_div_message_box_btn_like)

        let img_div_message_box_btn_like = document.createElement("img")
        img_div_message_box_btn_like.src = "img/likeB.png"
        div_message_box_btn_like.appendChild(img_div_message_box_btn_like)
    }



    let div_message_box_btn_message = document.createElement("div")
    div_message_box_btn_message.className = "message_box_btn_message " + message_mid;
    div_message_box_btn_message.setAttribute("alt", message_mid)
    div_message_box_btn_message.onclick = function() {
        let message_mid = this.getAttribute('alt');
        // console.log(message_mid);
        message_box_other_message_load_diplay_flex(message_mid)

    }
    div_message_box_btn.appendChild(div_message_box_btn_message)

    let a_div_message_box_btn_message = document.createElement("a")
    a_div_message_box_btn_message.textContent = "回應 (" + message_reply_number + ")"
    a_div_message_box_btn_message.id = "a_div_message_box_btn_message_" + message_mid
    div_message_box_btn_message.appendChild(a_div_message_box_btn_message)

    let img_div_message_box_btn_message = document.createElement("img")
    img_div_message_box_btn_message.className = "img_div_message_box_btn_message " + message_mid
    img_div_message_box_btn_message.src = "img/chat.png"
    div_message_box_btn_message.appendChild(img_div_message_box_btn_message)

    // 回應
    let div_message_box_other_message = document.createElement("div")
    div_message_box_other_message.className = "message_box_other_message " + message_mid
    div_predict_message.appendChild(div_message_box_other_message)



    if (message_reply_data.data) {
        // console.log(message_reply_data.message_predict_reply_load_data);
        for (let i = 0; i < message_reply_data.message_predict_reply_load_data.length; i++) {

            message_reply_data_ = message_reply_data.message_predict_reply_load_data[i]
            box_other_write_message_reply_add(message_reply_data_.message_mid, message_reply_data_.message_reply_mid, message_reply_data_.message_reply_user_imgsrc, message_reply_data_.message_reply_user_name, message_reply_data_.message_reply_text, message_reply_data_.message_reply_time, message_reply_data_.message_reply_time_about)
        }
    }
    let div_message_box_other_message_write = document.createElement("div")
    div_message_box_other_message_write.className = "message_box_other_message_write"
    div_message_box_other_message.appendChild(div_message_box_other_message_write)

    let textarea_message_box_other_message_write = document.createElement("textarea")
    textarea_message_box_other_message_write.placeholder = "分享一下你的想法... "
    textarea_message_box_other_message_write.className = "textarea_message_box_other_message_write " + message_mid
    textarea_message_box_other_message_write.setAttribute("alt", message_mid)
    textarea_message_box_other_message_write.setAttribute("onKeyDown", "check_input_(this.value,this.getAttribute('alt'))")
    textarea_message_box_other_message_write.setAttribute("onKeyUp", "check_input_(this.value,this.getAttribute('alt'))")

    div_message_box_other_message_write.appendChild(textarea_message_box_other_message_write)


    let img_message_box_other_message_write = document.createElement("img")
    img_message_box_other_message_write.src = "img/sent.png "
    img_message_box_other_message_write.setAttribute("alt", message_mid)

    img_message_box_other_message_write.onclick = function() {
        let message_mid = this.getAttribute('alt');
        box_other_write_message_reply(message_mid)
    }
    div_message_box_other_message_write.appendChild(img_message_box_other_message_write)

    let a_message_box_text_btn_error_text = document.createElement("a")
    a_message_box_text_btn_error_text.className = "message_box_text_btn_error_text " + message_mid
    a_message_box_text_btn_error_text.textContent = "."
    div_message_box_other_message.appendChild(a_message_box_text_btn_error_text)


}


/*-----------------------------*/
// 讀取全部的預測留言
function member_predict_load_message() {
    check_onload = false;

    if (forum_page == 0) {
        document.querySelector('.main_left_center').innerText = ""
    }
    fetch("/api/message_predict_load?data_number=" + String(forum_page)).then(function(response) {
        return response.json();
    }).then(function(result) {
        console.log(result)
        if (result.data.nodata) {
            document.querySelector('.base_load_gif_forum').style.display = "none";

        }
        if (result.data[0].predict_load) {

            for (let i = 0; i < result.data.length; i++) {
                predict_stock = result.data[i].stock_id + "－" + result.data[i].stock_name
                if (result.data[i].predict == "1") {
                    predict_trend = "漲"
                }
                if (result.data[i].predict == "-1") {
                    predict_trend = "跌"
                }
                if (result.data[i].predict == "0") {
                    predict_trend = "持平"
                }
                predict_message = result.data[i].message_user_text
                predict_message_member_name = result.data[i].message_user_name
                predict_message_member_img_src = result.data[i].message_user_imgsrc

                // 讚
                login_member_name_good_have = result.data[i].login_member_name_good_have
                message_good_number = result.data[i].message_good_number

                //回覆
                message_reply_number = result.data[i].reply_message_number
                message_reply_data = result.data[i].reply_message_data

                time = result.data[i].message_time
                time_about = result.data[i].message_time_about


                message_mid = result.data[i].mid
                message_check_status = result.data[i].message_check_status
                    // console.log(predict_stock + predict_trend)
                member_predict_add_message(predict_stock, predict_trend, predict_message, predict_message_member_name, predict_message_member_img_src, time, time_about, message_mid, message_check_status, login_member_name_good_have, message_good_number, message_reply_number, message_reply_data)

            }
            document.querySelector('.base_load_gif_forum').style.display = "none";
            check_onload = true;
        }
    })


}

member_predict_load_message()

/*-----------------------------*/
// 新增讚
function predict_message_btn_enter_like(message_mid_like, message_member) {
    if (check_function_end) {
        check_function_end = false
        let message_mid_like_data = {
            "status": "like",
            "login_member_name": login_member_name,
            "login_member_email": login_member_email,
            "message_mid_like": message_mid_like,
            "message_member": message_member
        }
        fetch("/api/message_predict_like", {
                method: 'POST',
                body: JSON.stringify(message_mid_like_data),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(res => {
                return res.json();
            })
            .then(result => {
                // console.log(result);
                if (result.ok) {


                    document.querySelector('#' + message_mid_like + ">img").src = "img/likeA.png";

                    document.querySelector('#' + message_mid_like).onclick = function() {
                        predict_message_btn_enter_unlike(message_mid_like)


                    }
                    let good_int = parseInt(document.querySelector('#' + message_mid_like + ">a").textContent.split('讚 (')[1].split(')')[0]) + 1
                    let good_str = good_int.toString()
                    document.querySelector('#' + message_mid_like + ">a").textContent = '讚 (' + good_str + ')'
                    check_function_end = true
                }

            });
    }
}
// 解除讚
function predict_message_btn_enter_unlike(message_mid_like) {
    if (check_function_end) {
        check_function_end = false
        let message_mid_like_data = {
            "status": "unlike",
            "login_member_name": login_member_name,
            "login_member_email": login_member_email,
            "message_mid_like": message_mid_like
        }
        fetch("/api/message_predict_like", {
                method: 'POST',
                body: JSON.stringify(message_mid_like_data),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(res => {
                return res.json();
            })
            .then(result => {
                // console.log(result);
                if (result.ok) {

                    document.querySelector('#' + message_mid_like + ">img").src = "img/likeB.png"

                    document.querySelector('#' + message_mid_like).onclick = function() {
                        let message_mid = this.getAttribute('alt');
                        let message_member = document.querySelector('.message_box_title_name.' + message_mid).textContent
                            // console.log(message_member)
                        predict_message_btn_enter_like(message_mid, message_member)

                    }
                    let good_int = parseInt(document.querySelector('#' + message_mid_like + ">a").textContent.split('讚 (')[1].split(')')[0]) - 1
                    let good_str = good_int.toString()
                    document.querySelector('#' + message_mid_like + ">a").textContent = '讚 (' + good_str + ')'
                    check_function_end = true

                }

            });
    }
}
/*-----------------------------*/

//回應區顯示&隱藏
function message_box_other_message_load_diplay_flex(message_mid) {
    document.querySelector('.message_box_other_message.' + message_mid).style.display = "flex";

    document.querySelector('.message_box_btn_message.' + message_mid).onclick = function() {
        message_box_other_message_load_diplay_none(message_mid)
    }
    document.querySelector('.img_div_message_box_btn_message.' + message_mid).src = "img/chat_.png"
}

function message_box_other_message_load_diplay_none(message_mid) {
    document.querySelector('.message_box_other_message.' + message_mid).style.display = "none";
    document.querySelector('.message_box_btn_message.' + message_mid).onclick = function() {
        message_box_other_message_load_diplay_flex(message_mid)
    }
    document.querySelector('.img_div_message_box_btn_message.' + message_mid).src = "img/chat.png"
}

/*-----------------------------*/
// 傳送留言的回覆
function box_other_write_message_reply(message_mid) {
    if (check_function_end) {
        check_function_end = false

        let message_reply_text = document.querySelector('.textarea_message_box_other_message_write.' + message_mid).value;
        let box_other_write_message_reply_data = {
            "login_member_name": login_member_name,
            "login_member_img_src": login_member_img_src,
            "login_member_email": login_member_email,
            "message_mid": message_mid,
            "message_reply_text": message_reply_text
        }



        if (message_reply_text.length <= 50) {

            fetch("/api/message_predict_reply_add", {
                    method: 'POST',
                    // body: encodeURI(JSON.stringify(data)),
                    body: JSON.stringify(box_other_write_message_reply_data),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(res => {
                    return res.json();
                })
                .then(result => {
                    if (result.ok) {


                        box_other_write_message_reply_add(result.mid, result.mid_reply, login_member_img_src, login_member_name, message_reply_text, result.time, "剛剛");
                        document.querySelector('.textarea_message_box_other_message_write.' + message_mid).value = "";

                        "a_div_message_box_btn_message_" + message_reply_number

                        let reply_int = parseInt(document.querySelector('#a_div_message_box_btn_message_' + message_mid).textContent.split('回應 (')[1].split(')')[0]) + 1
                        let reply_str = reply_int.toString()
                        document.querySelector('#a_div_message_box_btn_message_' + message_mid).textContent = '回應 (' + reply_str + ')'
                        document.querySelector('.message_box_text_btn_error_text.' + message_mid).style.display = "none"

                        check_function_end = true

                    }
                    if (result.error) {
                        document.querySelector('.message_box_text_btn_error_text.' + message_mid).style.display = "flex";
                        document.querySelector('.message_box_text_btn_error_text.' + message_mid).textContent = result.message;
                        check_function_end = true
                    }
                })
        } else {
            document.querySelector('.message_box_text_btn_error_text.' + message_mid).textContent = "字數不得超過50字";
            check_function_end = true

        }
    }
}

// 增加回覆區物件
function box_other_write_message_reply_add(message_mid, reply_message_mid, reply_member_img_src, reply_member_name, reply_message_text, reply_time, reply_time_about) {


    let div_message_box_other_message = document.querySelector('.message_box_other_message.' + message_mid);


    let div_message_box_other_message_load = document.createElement("div");
    div_message_box_other_message_load.className = "message_box_other_message_load " + reply_message_mid;

    if (div_message_box_other_message.firstChild == null) {

        div_message_box_other_message.appendChild(div_message_box_other_message_load)
    } else {

        div_message_box_other_message.insertBefore(div_message_box_other_message_load, div_message_box_other_message.childNodes[0]);
        //父.insertBefore(加入，被加入)
    }


    let div_message_box_other_message_load_left = document.createElement("div");
    div_message_box_other_message_load_left.className = "message_box_other_message_load_left";
    div_message_box_other_message_load.appendChild(div_message_box_other_message_load_left);

    let img_div_message_box_other_message_load_left = document.createElement("img");
    img_div_message_box_other_message_load_left.src = reply_member_img_src;
    div_message_box_other_message_load_left.appendChild(img_div_message_box_other_message_load_left);


    let div_message_box_other_message_load_right = document.createElement("div")
    div_message_box_other_message_load_right.className = "message_box_other_message_load_right"
    div_message_box_other_message_load.appendChild(div_message_box_other_message_load_right)

    let a_message_box_other_message_load_right_name = document.createElement("a")
    a_message_box_other_message_load_right_name.className = "message_box_other_message_load_right_name"
    a_message_box_other_message_load_right_name.textContent = reply_member_name
    a_message_box_other_message_load_right_name.setAttribute("href", "/member?name=" + reply_member_name)

    div_message_box_other_message_load_right.appendChild(a_message_box_other_message_load_right_name)


    let span_message_box_other_message_load_right_text = document.createElement("span")
    span_message_box_other_message_load_right_text.className = "message_box_other_message_load_right_text"
    span_message_box_other_message_load_right_text.textContent = reply_message_text
    div_message_box_other_message_load_right.appendChild(span_message_box_other_message_load_right_text)

    let span_message_box_other_message_load_right_time = document.createElement("span")
    span_message_box_other_message_load_right_time.className = "message_box_other_message_load_right_time"
    span_message_box_other_message_load_right_time.textContent = reply_time_about
    span_message_box_other_message_load_right_time.setAttribute("title", reply_time)

    div_message_box_other_message_load_right.appendChild(span_message_box_other_message_load_right_time)



}


/*-----------------------------*/


//功能-畫面捲動監聽
window.addEventListener('scroll', function() {
    let webwarp = document.querySelector('.warp');
    if (10 > (webwarp.scrollHeight - window.pageYOffset - window.innerHeight) & check_onload == true & forum_page != null) {
        check_onload = false;
        forum_page += 1;
        // document.getElementById("loadgif").style.display = "flex";

        member_predict_load_message()
        document.querySelector('.base_load_gif_forum').style.display = "flex";

    }
})


/*-------------rnak----------------*/


let main_right_ranking = document.querySelector('.main_right_ranking')


function member_predict_add_rank(no, member_name, predict_win, predict_fail, predict_total, predict_win_rate, member_src) {
    let div_main_right_ranking_stock_box = document.createElement("div");
    div_main_right_ranking_stock_box.className = "main_right_ranking_stock box";
    main_right_ranking.appendChild(div_main_right_ranking_stock_box)

    let div_main_right_ranking_stock_no = document.createElement("div");
    div_main_right_ranking_stock_no.className = "main_right_ranking_stock_no";
    div_main_right_ranking_stock_no.textContent = no;
    div_main_right_ranking_stock_box.appendChild(div_main_right_ranking_stock_no)

    let div_main_right_ranking_stock_data = document.createElement("div");
    div_main_right_ranking_stock_data.className = "main_right_ranking_stock_data";
    div_main_right_ranking_stock_box.appendChild(div_main_right_ranking_stock_data)

    let div_main_right_rank_box = document.createElement("div");
    div_main_right_rank_box.className = "div_main_right_rank_box";
    div_main_right_rank_box.addEventListener('click', function() {
        location.href = '/member?name=' + member_name
    });
    div_main_right_ranking_stock_data.appendChild(div_main_right_rank_box)

    let img_main_right_ranking_stock_member_img = document.createElement("img");
    img_main_right_ranking_stock_member_img.src = member_src;
    div_main_right_rank_box.appendChild(img_main_right_ranking_stock_member_img);

    let div_main_right_ranking_stock_member_name = document.createElement("a");
    div_main_right_ranking_stock_member_name.className = "main_right_ranking_stock_member_name";
    // div_main_right_ranking_stock_member_name.setAttribute("href", "/member?name=" + member_name)

    div_main_right_ranking_stock_member_name.textContent = member_name;
    div_main_right_rank_box.appendChild(div_main_right_ranking_stock_member_name);

    let span_main_right_ranking_stock_rate = document.createElement("span");
    span_main_right_ranking_stock_rate.className = "main_right_ranking_stock rate"
    div_main_right_ranking_stock_data.appendChild(span_main_right_ranking_stock_rate)

    let a_ranking_stocktitle_1 = document.createElement("a");
    a_ranking_stocktitle_1.className = "ranking_stocktitle";
    a_ranking_stocktitle_1.textContent = "勝率：";
    span_main_right_ranking_stock_rate.appendChild(a_ranking_stocktitle_1)
    let a_ranking_stocktitle_text_1 = document.createElement("a");
    a_ranking_stocktitle_text_1.className = "ranking_stocktitle_text";
    a_ranking_stocktitle_text_1.textContent = predict_win_rate + " %";
    span_main_right_ranking_stock_rate.appendChild(a_ranking_stocktitle_text_1)


    let span_main_right_ranking_stock_success = document.createElement("span");
    span_main_right_ranking_stock_success.className = "main_right_ranking_stock success"
    div_main_right_ranking_stock_data.appendChild(span_main_right_ranking_stock_success)

    let a_ranking_stocktitle_2 = document.createElement("a");
    a_ranking_stocktitle_2.className = "ranking_stocktitle";
    a_ranking_stocktitle_2.textContent = "成功：";
    span_main_right_ranking_stock_success.appendChild(a_ranking_stocktitle_2)
    let a_ranking_stocktitle_text_2 = document.createElement("a");
    a_ranking_stocktitle_text_2.className = "ranking_stocktitle_text";
    a_ranking_stocktitle_text_2.textContent = predict_win + " 次";
    span_main_right_ranking_stock_success.appendChild(a_ranking_stocktitle_text_2)


    let span_main_right_ranking_stock_fail = document.createElement("span");
    span_main_right_ranking_stock_fail.className = "main_right_ranking_stock fail"
    div_main_right_ranking_stock_data.appendChild(span_main_right_ranking_stock_fail)

    let a_ranking_stocktitle_3 = document.createElement("a");
    a_ranking_stocktitle_3.className = "ranking_stocktitle";
    a_ranking_stocktitle_3.textContent = "失敗：";
    span_main_right_ranking_stock_fail.appendChild(a_ranking_stocktitle_3)
    let a_ranking_stocktitle_text_3 = document.createElement("a");
    a_ranking_stocktitle_text_3.className = "ranking_stocktitle_text";
    a_ranking_stocktitle_text_3.textContent = predict_fail + " 次";
    span_main_right_ranking_stock_fail.appendChild(a_ranking_stocktitle_text_3)


    let span_main_right_ranking_stock_tatal = document.createElement("span");
    span_main_right_ranking_stock_tatal.className = "main_right_ranking_stock tatal"
    div_main_right_ranking_stock_data.appendChild(span_main_right_ranking_stock_tatal)

    let a_ranking_stocktitle_4 = document.createElement("a");
    a_ranking_stocktitle_4.className = "ranking_stocktitle";
    a_ranking_stocktitle_4.textContent = "預測：";
    span_main_right_ranking_stock_tatal.appendChild(a_ranking_stocktitle_4)
    let a_ranking_stocktitle_text_4 = document.createElement("a");
    a_ranking_stocktitle_text_4.className = "ranking_stocktitle_text";
    a_ranking_stocktitle_text_4.textContent = predict_total + " 次";
    span_main_right_ranking_stock_tatal.appendChild(a_ranking_stocktitle_text_4)

}

function member_predict_rank_api_load() {
    fetch("/api/message_predict_rank?data_status=rate").then(function(response) {
        return response.json();
    }).then(function(result) {
        if (result.ok) {
            for (let i = 0; i < result.data.length; i++) {
                member_name = result.data[i].member_name;
                predict_win = result.data[i].predict_win
                predict_fail = result.data[i].predict_fail
                predict_total = result.data[i].predict_total
                predict_win_rate = result.data[i].predict_win_rate
                member_src = result.data[i].member_src
                    // console.log(i, member_name, predict_win, predict_fail, predict_total, predict_win_rate)
                member_predict_add_rank(i + 1, member_name, predict_win, predict_fail, predict_total, predict_win_rate, member_src)
            }
        }
        document.querySelector('.base_load_gif_forum_rank').style.display = "none";



    })

}
member_predict_rank_api_load()