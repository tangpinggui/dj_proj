// 点击上传文件 服务器
$(function () {
    var upBtn = $('#up-file');
    upBtn.change(function (event) {
        var file = this.files[0]; // 获取文件
        var fileData = new FormData;
        fileData.append('upfile', file);  // 需要将文件写入FormData中,再传给后端
        xfzajax.post({
            'url': '/cms/save_news/',
            'data': fileData,
            'contentType': false,  // 不到指定类型
            'processData': false,  // 不做处理，因为是文件
            'success': function (result) {
                if (result['code'] === 200) {
                    var url = result['data']['url'];
                    console.log(url);
                    var newsPic = $("input[name='thumbnail']");  // 将值显示在input标签框中
                    newsPic.val(url)
                } else {
                    xfzalert.alertError(result['message'])
                }
            }
        })
    })
});

/*
// 上传到七牛 de文件及进度条显示
$(function () {
    var progressGroup = $('#progress-group');  // 控制进度条是否显示
    var progressBar = $('.progress-bar');  // 控制进度条的宽度 和 内容
    // qiniu返回的数据 progress, error, complete
    function progress(response) {
        var persent = response.total.percent;
        var width = persent.toFixed(0) + '%';
        progressBar.css({'width': width});
        progressBar.text(width);
    }

    function error(er) {
        for (var i=1;i<10000;i++){
            console.log(i);
        window.messageBox.showError(er.message);
        progressGroup.hide();  // 隐藏 display=none
        var urlInput = $("input[name='thumbnail']");
        urlInput.val('哎呀呀，服务器被怪兽吃掉了。emmmmm...');
    }}

    function complete(response) {
        var key = response.key; // hash val
        var qnurl = qiniu.getUploadUrl();
        var fileurl = qnurl + key;
        var urlInput = $("input[name='thumbnail']");
        urlInput.val(fileurl);

        progressBar.css({'width': 0});
        progressBar.text(0);
        // progressBar.removeAttr('disabled');
        progressGroup.hide();  // 隐藏 display=none
    }

    var upBtn = $('#up-file');
    upBtn.change(function (event) {
        var file = this.files[0];  // 获取文件
        xfzajax.get({
            'url': '/cms/qntoken/',
            'success': function (result) {
                if (result['code'] === 200) {
                    var token = result['data']['token'];
                    var key = file.name;
                    var putExtra = {
                        fname: key,
                        params: {},
                        mimeType: ["image/png", "image/jpeg", "image/gif"]
                    };
                    var config = {
                        useCdnDomain: true,
                        region: qiniu.region.z2
                    };
                    var observable = qiniu.upload(file, key, token, putExtra, config);
                    observable.subscribe({
                        "next": progress,
                        "error": error,
                        "complete": complete,
                    });
                    progressGroup.show()  // 显示. display=block
                } else {
                    console.log(result['code'])
                }
            }
        });
    })
});
*/

// UEditor
$(function () {
    window.ue = UE.getEditor('editor', {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/'
    });
});

// 通过ajax发送news
$(function () {
    var sendBtn = $('#puBtn');
    sendBtn.click(function (envent) {
        envent.preventDefault();
        var title = $("input[name='title']").val();
        var desc = $("input[name='desc']").val();
        var category = $("select[name='category']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var content_html = ue.getContent();

        xfzajax.post({
            'url': '/cms/write/news/',
            'data': {
                'title': title,
                'desc': desc,
                'category': category,
                'thumbnail': thumbnail,
                'content': content_html
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    xfzalert.alertSuccess("发布新闻成功", function () {
                        window.location.reload()
                    });
                } else {
                    xfzalert.alertError(result['message'])
                }
            }
        })
    })
});