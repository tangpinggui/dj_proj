// 添加分类
$(function () {
   var add_category=$('.add-category');
   add_category.click(function () {
       xfzalert.alertOneInput({
           'title': '添加新闻分类',
           'placeholder': '输入新增的新闻分类',
           'confirmCallback': function (inputvalue) {
               xfzajax.post({
                   'url': '/cms/add_news_category/',
                   'data': {
                       'name': inputvalue
                   },
                   'success': function (result) {
                       if(result.code===200){
                           window.location.reload();
                       }else{
                           xfzalert.close();
                           window.messageBox.showError(
                               result['message']
                           )
                       }
                   }
               })
           }
       })
   })
});

// 编辑分类
$(function () {
    var editBtn = $('.edit-btn');
    editBtn.click(function () {
        var currentBtn=$(this);
        var oldValue = currentBtn.parent().parent();
        var pk = oldValue.attr('data-pk');
        var name = oldValue.attr('data-name');
        xfzalert.alertOneInput({
            'title': '修改分类',
            'text': 'input new category',
            'value': name,
            'confirmCallback': function (inputvalue) {
                 xfzajax.post({
                'url': '/cms/edit_news_category/',
                'data': {
                    'name': inputvalue,
                    'pk': pk
                },
                'success': function (result) {
                    if(result['code']===200){
                        window.location.reload()
                    }else{
                        xfzalert.close();
                        window.messageBox.showError(result['message'])
                    }
                }
            })
            }
        })
    })
});

// 删除分类
$(function () {
    var delBtn = $('.delete-btn');
    delBtn.click(function () {
        var currentBtn=$(this);
        var oldValue = currentBtn.parent().parent();
        var pk = oldValue.attr('data-pk');
        xfzalert.alertConfirm({
            'title': '危险操作',
            'text': '你确定要是删除该分类吗',
            'confirmCallback': function () {
                 xfzajax.post({
                'url': '/cms/del_news_category/',
                'data': {
                    'pk': pk
                },
                'success': function (result) {
                    if(result['code']===200){
                        window.location.reload()
                    }else{
                        xfzalert.close();
                        window.messageBox.showError(result['message'])
                    }
                }
            })
            }
        })
    })
});