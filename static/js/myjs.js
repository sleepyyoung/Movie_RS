// 禁用F5和F12
document.onkeydown = function () {
    if (event.keyCode === 116) {
        event.keyCode = 0;
        event.cancelBubble = true;
        return false;
    }
    // if (event.keyCode === 123) {
    //     event.keyCode = 0;
    //     event.cancelBubble = true;
    //     return false;
    // }
}
//禁用右键
document.oncontextmenu = function () {
    return false;
}

/************************ home ************************/
// js为ol添加内容 热搜榜
function now_realtimehot_content(data) {
    var obj = eval(data);
    var ol = $("<li></li>");
    var time = (obj[1]['datetime'].toString().replace("T", " "))
    ol.append(time)
    for (var i = 0; i < obj.length; i++) {
        var srank = obj[i]['srank']
        if (srank === 0) {
            srank = "[置顶位]"
        }
        var title = obj[i]['title']
        var heat = obj[i]['heat']
        var href = obj[i]['href']
        var tag = obj[i]['tag']
        if (tag !== '荐') {
            var li = $('<li><a href="' + href + '">' + srank + '. &nbsp;' + title + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + heat + '</a></li>');
        } else {
            li = $('<li><a>' + srank + '. [推荐位].&nbsp;' + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + '</a></li>');
        }
        ol.append(li);
    }
    $('#now_realtimehot li').replaceWith(ol);
}

// js为ol添加内容 要闻榜
function now_socialevent_content(data) {
    var obj = eval(data);
    var ol = $("<li></li>");
    var time = (obj[1]['datetime'].toString())
    ol.append(time)
    for (var i = 0; i < obj.length; i++) {
        var title = obj[i]['title']
        var href = obj[i]['href']
        var li = $('<li><a href="' + href + '">' + title + '</a></li>');
        ol.append(li);
    }
    $('#now_socialevent li').replaceWith(ol);
}

// 按照内容搜索时所触发的函数
function check_content_search_somethings(method) {
    var search_content = $("#search_content").val().replace(/(^\s*)|(\s*$)/g, "")
    if (method === 'fuzzy') {
        if (search_content === '') {
            alert("查找内容不能为空");
            return;
        }

        return {
            search_content: encodeURIComponent(search_content)
        }
    } else {
        return {
            search_content: encodeURIComponent(search_content)
        }
    }
}

// 发送邮箱验证码
function send_email_captcha(obj, time) {
    obj.disabled = true;
    setTimeout(function () {
        var x = setInterval(function () {
            time = time - 1000;
            obj.value = time / 1000;
            if (time === 0) {
                clearInterval(x);
                obj.value = "未收到?重新发送";
                obj.disabled = false;
            }
        }, 1000);
    });
}

// 显示提示
function alertmess(mess) {
    $('#alertmess').html(mess);  // 填入要显示的文字
    $('#alertmess').show();  // 显示弹框
    setTimeout(function () {  // 倒计时
        $('#alertmess').html(''); // 清空文本
        $('#alertmess').hide();  // 隐藏弹框
    }, 2000);
}

//导出为xlsx
function table2xlsx(filename) {
    $(".table2local").table2excel({
        name: "xlsx",
        filename: filename,
        fileext: ".xlsx",
        exclude_img: true,
        exclude_links: true,
        exclude_inputs: true
    });
}

//导出为xls
function table2xls(filename) {
    $(".table2local").table2excel({
        name: "xlx",
        filename: filename,
        fileext: ".xls",
        exclude_img: true,
        exclude_links: true,
        exclude_inputs: true
    });
}

// 导出为csv
function table2csv(filename) {
    var all_contents = "\uFEFF";
    var one = $("#pstable > thead > tr > th")
    for (var i = 0; i < one.length; i++) {
        var th = one[i];
        all_contents += th.innerHTML.toString();
        if (i < one.length - 1) {
            all_contents += ",";
        } else {
            all_contents += "\n";
        }

    }
    var table_lists = $("#pstable > tbody > tr")
    for (var i = 0; i < table_lists.length; i++) {
        var tr = table_lists[i];
        var _td = tr.children
        for (var j = 0; j < _td.length; j++) {
            var td = _td[j];
            all_contents += td.innerHTML.toString().replace("<a>", "").replace("</a>", "");
            if (j < _td.length - 1) {
                all_contents += ","
            } else {
                all_contents += "\n"
            }
        }
    }

    var blob = new Blob([all_contents], {type: "text/plain;charset=utf-8"});
    saveAs(blob, filename);
}

//导出为图片
function table2img(filename) {
    domtoimage.toBlob(document.getElementById('pstable'))
        .then(function (blob) {
            window.saveAs(blob, filename);
        });
}


/************************ realtimehot_search_by_time ************************/

// 页面tr推荐位点击提示
function tr_onclick_realtimehot(tag, href) {
    if (tag === '荐') {
        alertmess('这个就算了，推荐位又没给我钱');
    } else {
        window.open(href)
    }
}


// js为tbody添加内容
function add_tbody_content_realtimehot(data) {
    var obj = eval(data);
    var tbody = $('<tbody></tbody>');
    for (var i = 0; i < obj.length; i++) {
        var srank = obj[i]['srank']
        if (srank === 0) {
            srank = "置顶位"
        }
        var title = obj[i]['title']
        var heat = obj[i]['heat']
        var tag = obj[i]['tag']
        var href = obj[i]['href']
        var time = (obj[i]['datetime'].toString().replace("T", " "))

        var tr = $('<tr onclick="' + 'tr_onclick_realtimehot(' + '\'' + tag + '\'' + ',' + '\'' + href + '\'' + ')"' + '></tr>');
        if (tag === '荐') {
            tr.append('<td><a>' + srank +
                '</a></td>' + '<td><a>' +
                '</a></td>' + '<td><a>' +
                '</a></td>' + '<td><a>' + tag +
                '</a></td>' + '<td><a>' + time +
                '</a></td>');
        } else {
            tr.append('<td><a>' + srank +
                '</a></td>' + '<td><a>' + title +
                '</a></td>' + '<td><a>' + heat +
                '</a></td>' + '<td><a>' + tag +
                '</a></td>' + '<td><a>' + time +
                '</a></td>');
        }
        tbody.append(tr);
    }
    $('#pstable tbody').replaceWith(tbody);
}


// 格式化时间戳
function whether2(m) { //判断是否是两个字符
    return m < 10 ? '0' + m : m
}

function format(timestamp) {
    var time = new Date(timestamp);
    var y = time.getFullYear();
    var m = time.getMonth() + 1;
    var d = time.getDate();
    var h = time.getHours();
    var mm = time.getMinutes();
    var s = time.getSeconds();
    return y + '-' + whether2(m) + '-' + whether2(d) + 'T' + whether2(h) + ':' + whether2(mm) + ':' + whether2(s);
}

// 显示当前时间
function showTime() {
    var date = new Date();
    var now_year = whether2(date.getFullYear().toString())
    var now_month = whether2((date.getMonth() + 1).toString())
    var now_day = whether2(date.getDate().toString())
    var now_hour = whether2(date.getHours().toString())
    var now_minute = whether2(date.getMinutes().toString())
    var now_second = whether2(date.getSeconds().toString())
    document.getElementById("current_time").innerText = "当前时间 : " + now_year + "-" + now_month + "-" + now_day + " " + now_hour + ":" + now_minute + ":" + now_second;
}

// 设置时间搜索默认值为当前时间
function setTime() {
    var date = new Date();
    var now_year = whether2(date.getFullYear().toString())
    var now_month = whether2((date.getMonth() + 1).toString())
    var now_day = whether2(date.getDate().toString())
    var now_hour = whether2(date.getHours().toString())
    var now_minute = whether2(date.getMinutes().toString())
    document.getElementById("now_year").innerHTML = now_year.toString();
    document.getElementById("now_month").innerHTML = now_month.toString();
    document.getElementById("now_day").innerHTML = now_day.toString();
    document.getElementById("now_hour").innerHTML = now_hour.toString();
    document.getElementById("now_minute").innerHTML = now_minute.toString();
}