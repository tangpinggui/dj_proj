// 选择时间事件
$(function () {
    var today = new Date();
    var todayStr = today.getFullYear() + '/' + (today.getMonth() + 1)
        + '/' + today.getDate();
    var option = {
        'format': 'yyyy/mm/dd',
        'autoclose': true,
        'startDate': '2018/7/10',
        'endDate': todayStr,
        'language': 'zh-CN',
        'todayBtn': 'linked', // 显示一个选择今日的按钮
        'todayHighlight': true, // 当前日期是否高亮
        'showButtonPanel': false, // 是否展示按钮
        'clearBtn': true

        // 'startDate': '-3d'
    };
    $('input[name="start"]').datepicker(option);
    $('input[name="end"]').datepicker(option);
});


// 删除新闻事件
$(function () {
    var delBtn = $('.del-btn');
    delBtn.click(function () {
        var pk = $(this).attr('pk');
        xfzalert.alertConfirm({
            "title": "谨慎操作",
            "text": "您确认删除吗",
            "confirmCallback": function () {
                xfzajax.post({
                    url: '/cms/del_news/',
                    data: {'pk': pk},
                    success: function (result) {
                        if (result['code'] === 200) {
                            xfzalert.alertSuccess("删除成功",function () {
                                // window.location.reload()
                                window.location = window.location.href
                            })
                        } else {
                            window.messageBox.showError(result.message)
                        }
                    }
                })
            }
        })
    })
})
