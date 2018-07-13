// art-template 过滤器  dateFormat为过滤器的名字
$(function () {
    template.defaults.imports.timeSince = function (date) {
        var date = new Date(date);
        var value = date.getTime();  // 毫秒
        var now = (new Date()).getTime();
        var timestamp = (now - value) / 1000;  // 转换成秒
        if (timestamp < 60) {
            return '刚刚'
        } else if (timestamp >= 60 && timestamp < 60 * 60) {
            minutes = parseInt(timestamp / 60)
            return minutes + '分钟前'
        }
        else if (timestamp >= 60 * 60 && timestamp < 60 * 60 * 24) {
            hours = parseInt(timestamp / 60 / 60)
            return hours + '小时前'
        }
        else if (timestamp >= 60 * 60 * 24 && timestamp < 60 * 60 * 24 * 30) {
            days = parseInt(timestamp / 60 / 60 / 24)
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
});

// art-template  each事件
$(function () {
    var loadMoreBtn = $('.load-more-btn');
    var page = 2;
    loadMoreBtn.click(function () {
        xfzajax.get({
            'url': '/news_list/',
            'data': {
                'page': page
            },
            'success': function (result) {
                var newses = result['data'];
                var newsListGroup = $('.news-list-group');
                var tpl = template("news-item", {"newses": newses});
                if (newses.length > 0) {
                    newsListGroup.append(tpl);
                    page++;
                } else {
                    window.messageBox.showInfo("no much more data");
                }
            }
        })
    })
});