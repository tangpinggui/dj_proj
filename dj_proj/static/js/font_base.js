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

$(function () {
   var menuLi = $('.menu li');
   menuLi.click(function () {
       var index = $(this);
       menuLi[index].addClass('active');
       if(index>1){
           menuLi[index-1].removeClass('active')
       }
   })
});