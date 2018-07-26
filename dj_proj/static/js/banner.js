// 移除添加轮播图的模板
// 每一个bannerItem都分别有closeBtn.click事件
function closeEvent(bannerItem) {
    var closeBtn = bannerItem.find('.banner-close-btn');  //
    // var banner_id = bannerItem.find('.banner-son').attr('banner-id');  error
    // bannerItem是通过last或者first选择的，它是一个标签， 见creatBannerItem()
    var banner_id = bannerItem.attr('banner-id');
    closeBtn.click(function () {
        if (banner_id) {
            xfzalert.alertConfirm({
                'title': '谨慎操作',
                'text': '你确定要删除该轮播图吗？',
                'confirmCallback': function () {
                    xfzajax.post({
                        url: '/cms/delete_banner/',
                        data: {
                            'banner_id': banner_id
                        },
                        'success': function (result) {
                            if (result['code'] === 200) {
                                bannerItem.remove();
                                window.messageBox.showSuccess('删除成功')
                            }
                        }
                    })
                }
            })
        } else {
            bannerItem.remove()
        }
    })
}

// 上传轮播图图片
function addSelectEvent(bannerItem) {
    var addImage = bannerItem.find('.add-image');
    var addImageInput = bannerItem.find('.add-image-input');
    addImage.click(function () {
        addImageInput.click()
    });
    // 选择图片后，用changes事件的this.files获取
    addImageInput.change(function () {
        var file = this.files[0];
        // FormData存储file对象，通过append('key', 'val)
        var dataForm = new FormData;
        dataForm.append('upfile', file);
        xfzajax.post({
            'url': '/cms/save_news/',
            'data': dataForm,
            'processData': false, // 传输文件需要指定的参数
            'contentType': false,
            'success': function (result) {
                if (result['code'] == 200) {
                    var url = result.data.url;
                    addImage.attr('src', url);
                    addImage.addClass("new-img-url")
                }
            }
        })
    })
}

// 添加banner detail
function addBannerDetail(bannerItem) {
    var commitBtn = bannerItem.find('#commit-btn');

    commitBtn.click(function () {
        var addImage = bannerItem.find('.new-img-url');
        if (!addImage.length) {
            xfzalert.alertInfo("请选择图片")
        } else {
            var image_url = addImage.attr('src');
            var priority = bannerItem.find('.priority').val();
            var jump_link = bannerItem.find('.jump-link').val();
            var banner_id = bannerItem.attr('banner-id');
            var url = null;
            if (banner_id) {
                url = '/cms/change_banner/'
            } else {
                url = '/cms/add_banners/'
            }
            xfzajax.post({
                'url': url,
                'data': {
                    'image_url': image_url,
                    'priority': priority,
                    'jump_link': jump_link,
                    'banner_id': banner_id
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        console.log(result);
                        //2. var banner_id = undefined  操作1，相当于操作 2
                        if (!banner_id) {
                            //1. var banner_id = result.data['banner_id'];  var 定义变量会在函数前面先声明
                            banner_id = result.data['banner_id'];
                        }
                        bannerItem.attr('banner-id', banner_id);
                        var priorityShow = bannerItem.find('.priority-show');
                        priorityShow.text('优先级： ' + priority);
                        window.messageBox.showSuccess(result.message)
                    } else {
                        window.messageBox.showInfo(result.message)
                    }
                }
            })
        }
    })
}

// 添加轮播图
$(function () {
    var addBtn = $('#add-btn');
    var bannerBox = $('.banner-box');
    addBtn.click(function () {
        // art-template模板
        /*
        var tpl = template('banner-item');  // 模板内容
        var bannerBox = $('.banner-box');  // 装模板的盒子
        bannerBox.prepend(tpl);  // 装进盒子
        var bannerItem = bannerBox.find('.banner-son:first');  // 找到最后装进盒子的子元素
        closeEvent(bannerItem);
        addSelectEvent(bannerItem);
        addBannerDetail(bannerItem)

        // 等同creatBannerItem()
        */
        var chirldens = bannerBox.children();
        if (chirldens.length >= 6) {
            xfzalert.alertInfo("只能添加6个轮播图")
        } else {
            creatBannerItem()
        }
    })
});

// 重构bannerItem代码
function creatBannerItem(banner) {
    // 如果没有接受banner参数，则为undefined类型
    var tpl = template('banner-item', {'banner': banner});
    var bannerBox = $('.banner-box');  // 装模板的盒子
    var bannerItem = '';
    if (banner) {
        bannerBox.append(tpl);  // 装进盒子
        bannerItem = bannerBox.find('.banner-son:last');  // 找到最后装进盒子的子元素, className为banner-son的最后的标签
    } else {
        bannerBox.prepend(tpl);
        bannerItem = bannerBox.find('.banner-son:first');  // 找到最后装进盒子的子元素
    }
    closeEvent(bannerItem);
    addSelectEvent(bannerItem);
    addBannerDetail(bannerItem)
}

// 加载页面后显示已经添加轮播图
$(function () {
    xfzajax.post({
        'url': '/cms/banner_list/',
        'success': function (result) {
            var banners = result['data']['banners'];
            for (var i = 0; i < banners.length; i++) {
                var banner = banners[i];
                /*
                var tpl = template('banner-item', {'banner': banner});
                var bannerBox = $('.banner-box');  // 装模板的盒子
                bannerBox.append(tpl);  // 装进盒子
                // 等同creatBannerItem(banner)
                */
                creatBannerItem(banner)
            }
        }
    })
});