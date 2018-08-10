$(function () {
    var telephone = $('.edit-delete-staff');
    var deleteBtn = $('.delete-btn');
    deleteBtn.click(function () {
        var telephone = $(this).parent().parent().attr('telephone');
        xfzalert.alertConfirm({
            title: '谨慎操作',
            text: '您确认移除该员工吗？',
            confirmCallback: function () {
                xfzajax.post({
                    url: '/cms/del_staff/',
                    data: {
                        telephone: telephone
                    },
                    success: function (result) {
                        if (result['code'] === 200) {
                            // xfzalert.alertSuccess('删除成功');
                            window.messageBox.showSuccess('删除成功1');
                            window.location=window.location.href
                        }else {
                            window.messageBox.showError(result.message)
                        }
                    }
                })
            }

        });
    })
});