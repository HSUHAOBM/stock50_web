let check_function_end = true;
let forum_page = 0;
let check_onload = true;


// 預測留言根據選擇變化
function stock_select_change() {
    let stock_select_textContent = document.querySelector('.stock_select_list');
    let index = stock_select_textContent.selectedIndex
    let stock_select_out_text = stock_select_textContent.options[index].text
    document.querySelector('.member_out_stock.name').textContent = stock_select_out_text;
    document.querySelector('.member_out_text').style.display = "flex";
    document.querySelector('.textInput').placeholder = "分享你對 " + stock_select_out_text + " 的想法 ...";

}

function trend_radio_change(text) {
    document.querySelector('.member_out_stock.trend').textContent = " " + text;
    document.querySelector('.member_out_text').style.display = "flex";

}


// 送出預測
let member_predict_data_form = document.getElementById('member_predict_data');
member_predict_data_form.addEventListener('submit', function(event) {
    if (check_function_end) {
        check_function_end = false
        var member_predict_data_form_ = new FormData(member_predict_data_form);
        let member_predict_form_data = {};
        event.preventDefault();
        // predict_message = replaceTextarea1(member_predict_data_form_.get("member_predict_message"))
        predict_message = member_predict_data_form_.get("member_predict_message")
            // console.log(predict_message.replace(/\n|\r\n/g, "<br>"))
        member_predict_form_data = {
                "predict_stock": member_predict_data_form_.get("member_predict_stock"),
                "predict_trend": member_predict_data_form_.get("member_predict_trend"),
                "predict_message": predict_message,
                "login_member_name": login_member_name,
                "login_member_email": login_member_email,
                "login_member_img_src": login_member_img_src
            }
            // console.log(member_predict_form_data);

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
    a_message_box_title_name.className = "message_box_title_name"
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
            predict_message_btn_enter_like(message_mid)

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

    /*-- -- -- -- - */

    // let div_message_box_other_message_load = document.createElement("div")
    // div_message_box_other_message_load.className = "message_box_other_message_load " + message_mid
    // div_message_box_other_message.appendChild(div_message_box_other_message_load)

    // let div_message_box_other_message_load_left = document.createElement("div")
    // div_message_box_other_message_load_left.className = "message_box_other_message_load_left"
    // div_message_box_other_message_load.appendChild(div_message_box_other_message_load_left)

    // let img_div_message_box_other_message_load_left = document.createElement("img")
    // img_div_message_box_other_message_load_left.src = "img/1.jpg "
    // div_message_box_other_message_load_left.appendChild(img_div_message_box_other_message_load_left)


    // let div_message_box_other_message_load_right = document.createElement("div")
    // div_message_box_other_message_load_right.className = "message_box_other_message_load_right"
    // div_message_box_other_message_load.appendChild(div_message_box_other_message_load_right)

    // let span_message_box_other_message_load_right_name = document.createElement("span")
    // span_message_box_other_message_load_right_name.className = "message_box_other_message_load_right_name"
    // span_message_box_other_message_load_right_name.textContent = "HAO"
    // div_message_box_other_message_load_right.appendChild(span_message_box_other_message_load_right_name)

    // let span_message_box_other_message_load_right_text = document.createElement("span")
    // span_message_box_other_message_load_right_text.className = "message_box_other_message_load_right_text"
    // span_message_box_other_message_load_right_text.textContent = "真的嗎?"
    // div_message_box_other_message_load_right.appendChild(span_message_box_other_message_load_right_text)

    // let span_message_box_other_message_load_right_time = document.createElement("span")
    // span_message_box_other_message_load_right_time.className = "message_box_other_message_load_right_time"
    // span_message_box_other_message_load_right_time.textContent = "2021/7/10 14:47"
    // div_message_box_other_message_load_right.appendChild(span_message_box_other_message_load_right_time)

    /*-- -- -- -- - */


    let div_message_box_other_message_write = document.createElement("div")
    div_message_box_other_message_write.className = "message_box_other_message_write"
    div_message_box_other_message.appendChild(div_message_box_other_message_write)

    let textarea_message_box_other_message_write = document.createElement("textarea")
    textarea_message_box_other_message_write.placeholder = "分享一下你的想法... "
    textarea_message_box_other_message_write.className = "textarea_message_box_other_message_write " + message_mid
    div_message_box_other_message_write.appendChild(textarea_message_box_other_message_write)

    let img_message_box_other_message_write = document.createElement("img")
    img_message_box_other_message_write.src = "img/sent.png "
    img_message_box_other_message_write.setAttribute("alt", message_mid)

    img_message_box_other_message_write.onclick = function() {
        let message_mid = this.getAttribute('alt');
        // console.log(document.querySelector('.textarea_message_box_other_message_write.' + message_mid).value)
        // console.log(message_mid)
        box_other_write_message_reply(message_mid)
    }
    div_message_box_other_message_write.appendChild(img_message_box_other_message_write)

    let a_message_box_text_btn_error_text = document.createElement("a")
    a_message_box_text_btn_error_text.className = "message_box_text_btn_error_text " + message_mid
    a_message_box_text_btn_error_text.textContent = ".2222222222"
    div_message_box_other_message.appendChild(a_message_box_text_btn_error_text)


}




// 讀取全部的預測留言
function member_predict_load_message() {
    fetch("/api/message_predict_load?data_number=" + String(forum_page)).then(function(response) {
        return response.json();
    }).then(function(result) {


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

        check_onload = true;
    })
}

member_predict_load_message()

// 新增讚
function predict_message_btn_enter_like(message_mid_like) {
    if (check_function_end) {
        check_function_end = false
        let message_mid_like_data = {
            "status": "like",
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
                console.log(result);
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
                console.log(result);
                if (result.ok) {

                    document.querySelector('#' + message_mid_like + ">img").src = "img/likeB.png"

                    document.querySelector('#' + message_mid_like).onclick = function() {
                        let message_mid = this.getAttribute('alt');
                        predict_message_btn_enter_like(message_mid)

                    }
                    let good_int = parseInt(document.querySelector('#' + message_mid_like + ">a").textContent.split('讚 (')[1].split(')')[0]) - 1
                    let good_str = good_int.toString()
                    document.querySelector('#' + message_mid_like + ">a").textContent = '讚 (' + good_str + ')'
                    check_function_end = true

                }

            });
    }
}

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
                    check_function_end = true

                }
                if (result.error) {
                    document.querySelector('.message_box_text_btn_error_text.' + message_mid).style.display = "flex";
                    document.querySelector('.message_box_text_btn_error_text.' + message_mid).textContent = result.message;
                    check_function_end = true
                }
            })
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




//功能-畫面捲動監聽
window.addEventListener('scroll', function() {
    let webwarp = document.querySelector('.warp');
    if (10 > (webwarp.scrollHeight - window.pageYOffset - window.innerHeight) & check_onload == true & forum_page != null) {
        check_onload = false;
        forum_page += 1;
        // document.getElementById("loadgif").style.display = "flex";

        member_predict_load_message()
    }
})