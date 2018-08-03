// UEditor
$(function () {
    window.ue = UE.getEditor('profile-input', {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/'
    });
});

$(function () {
   var pubCourse = $("#pub-course") ;
   pubCourse.click(function (event) {
       event.preventDefault();
       var title = $('#title-input').val();
       var category = $('#category-input').val();
       var teacher = $('#teacher-input').val();
       var video = $('#video-input').val();
       var cover = $('#cover-input').val();
       var price = $('#price-input').val();
       var duration = $('#duration-input').val();
       var profile = ue.getContent();
       xfzajax.post({
           'url': '',
           'data': {
               'title': title,
               'category_id': category,
               'teacher_id': teacher,
               'video_url': video,
               'cover_url': cover,
               'price': price,
               'duration': duration,
               'profile': profile
           },
           'success': function (result) {
               if(result.code === 200){
                   xfzalert.alertSuccess("课程发布成功", function () {
                       window.location = window.location.href
                   })
               }else {
                   window.messageBox.showError(result['message'])
               }
           }
       })
   })
});