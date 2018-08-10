// art-template 过滤器  timeSince为过滤器的名字
$(function () {
    if (template) {
        template.defaults.imports.timeSince = function (date) {
            var date = new Date(date);
            var value = date.getTime();  // 毫秒
            var now = (new Date()).getTime();
            var timestamp = (now - value) / 1000;  // 转换成秒
            if (timestamp < 60) {
                return '刚刚'
            } else if (timestamp >= 60 && timestamp < 60 * 60) {
                minutes = parseInt(timestamp / 60);
                return minutes + '分钟前'
            }
            else if (timestamp >= 60 * 60 && timestamp < 60 * 60 * 24) {
                hours = parseInt(timestamp / 60 / 60);
                return hours + '小时前'
            }
            else if (timestamp >= 60 * 60 * 24 && timestamp < 60 * 60 * 24 * 30) {
                days = parseInt(timestamp / 60 / 60 / 24);
                return days + '天前'
            }
            else {
                year = date.getFullYear();
                month = date.getMonth();
                day = date.getDay();
                hours = date.getHours();
                minutes = date.getMinutes();
                return year + '/' + month + '/' + day + ' ' + hours + ':' + minutes
            }
        };
    }
});

// $(function () {
//    var menuLi = $('.menu li');
//    menuLi.click(function () {
//        var index = $(this);
//        menuLi[index].addClass('active');
//        if(index>1){
//            menuLi[index-1].removeClass('active')
//        }
//    })
// });

$(function () {
    // http://127.0.0.1:8000/path/path1/?xx=xxx
    var url1 = window.location.href;
    // http://127.0.0.1:8000/path/path1/
    var url = url1.split('?')[0];
    // http:
    var protocol = window.location.protocol;
    // 127.0.0.1:8000
    var host = window.location.host;
    // http://127.0.0.1:8000
    var domain = protocol + '//' + host;
    // /path/path1/
    var path = url.replace(domain,'');
    var menuLis = $(".menu li");
    for(var index=0;index<menuLis.length;index++){
        var li = $(menuLis[index]);
        var a = li.children("a");
        var href1 = a.attr('href');  // /path/path1/?xx=xxx
        var href = href1.split('?')[0];  // /path/path1/
        if(href === path){  // 浏览器url和a标签url比较，相同则表示设置为选中 active
            li.addClass('active');
        }
    }
});