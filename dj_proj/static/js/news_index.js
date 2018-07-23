// art-template  each事件
//加载新闻
$(function () {
    var loadMoreBtn = $('.load-more-btn');
    var li = $('.list-tab-group li.active');
    loadMoreBtn.click(function () {
        var page = parseInt(loadMoreBtn.attr('page'));
        var li = $('.list-tab-group li.active');
        var category_id = li.attr('category-id');
        console.log("category,page",category_id,page)
        xfzajax.get({
            'url': '/news_list/',
            'data': {
                'page': page,
                'category_id': category_id
            },
            'success': function (result) {
                var newses = result['data'];
                var newsListGroup = $('.news-list-group');
                var tpl = template("news-item", {"newses": newses});
                if (newses.length > 0) {
                    newsListGroup.append(tpl);
                    page++;
                    loadMoreBtn.attr('page', page)
                } else {
                    window.messageBox.showInfo("no much more data");
                }
            }
        })
    })
});

// 切换新闻分类
$(function () {
    var listTabGroup = $('.list-tab-group');
    var liGroup = listTabGroup.children();
    liGroup.click(function () {
        var li = $(this);
        var category_id = li.attr('category-id');
        xfzajax.get({
            'url': '/news_list/',
            'data': {
                'category_id': category_id
            },
            'success': function (result) {
                var newses = result['data'];
                var newsListGroup = $('.news-list-group');
                var tpl = template("news-item", {"newses": newses});
                var loadMoreBtn = $('.load-more-btn');

                newsListGroup.empty();  // 清空之前存在的新闻
                newsListGroup.append(tpl);
                li.addClass('active').siblings().removeClass('active')
                loadMoreBtn.attr('page', 2);
            }
        })
    })
});
