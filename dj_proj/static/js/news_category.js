

// 添加分类
$(function () {
    var addBtn = $("#add-btn");
    addBtn.click(function () {
        xfzalert.alertOneInput({
            'title': '添加新闻分类',
            'placeholder': '请输入新闻分类',
            'confirmCallback': function (inputValue) {
                xfzajax.post({
                    'url': '/cms/add_news_category/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (result) {
                        if(result['code'] === 200){
                            window.location.reload();
                        }else{
                            xfzalert.close();
                            window.messageBox.showError(result['message']);
                        }
                    }
                });
            }
        });
    });
});

// 编辑分类
$(function () {
    var editBtn = $('.edit-btn');
    editBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        var name = tr.attr('data-name');
        xfzalert.alertOneInput({
            'title': '请输入新名称',
            'placeholder': '请输入分类名称',
            'value': name,
            'confirmCallback': function (inputValue) {
                xfzajax.post({
                    'url': '/cms/edit_news_category/',
                    'data': {
                        'pk': pk,
                        'name': inputValue
                    },
                    'success': function (result) {
                        if(result['code'] === 200){
                            window.location.reload();
                        }
                    }
                });
            }
        });
    });
});

// 删除分类
$(function () {
    var deleteBtn = $('.delete-btn');
    deleteBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        xfzalert.alertConfirm({
            'text': '您确定要删除这个分类吗？',
            'confirmCallback': function () {
                xfzajax.post({
                    'url': '/cms/delete_news_category/',
                    'data': {
                        'pk': pk
                    },
                    'success': function (result) {
                        if(result['code'] === 200){
                            window.location.reload();
                        }
                    }
                });
            }
        });
    });
});
