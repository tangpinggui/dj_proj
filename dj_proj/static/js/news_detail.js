// 发送评论信息
$(function () {
    var submitBtn = $('#submit-comment-btn');
    var textarea = $('#comment-textarea');
    var news_id = submitBtn.attr('data-news-id');
    submitBtn.click(function (event) {
        event.preventDefault();
        var content = textarea.val();
        xfzajax.post({
            'url': '/add_news_comment/',
            'data': {
                'content': content,
                'news_id': news_id
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var comment = result['data'];
                    var tpl = template('comment-item', {'comment': comment});
                    var box = $('.comment-list-group');
                    box.prepend(tpl)
                    textarea.val('')
                } else {
                    window.messageBox.showInfo(result['message'])
                }
            }
        })
    })
});