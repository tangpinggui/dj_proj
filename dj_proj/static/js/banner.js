function closeEvent(bannerItem) {
    var closeBtn = bannerItem.find('.close-btn');
    closeBtn.click(function () {
        console.log('?')
        bannerItem.remove()
    })
}

$(function () {
    var addBtn = $('#add-btn');
    addBtn.click(function () {
        var tpl = template('banner-item');
        var bannerBox = $('.banner-box');
        bannerBox.append(tpl);
        var bannerItem = bannerBox.find('.banner-son:last');
        closeEvent(bannerItem)
    })
});

