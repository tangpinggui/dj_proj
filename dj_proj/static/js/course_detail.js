$(function () {
    var span = $(".video-container span");
    var video_url = span.attr("data-video-url");
    var cover_url = span.attr('data-cover-url');
    var course_id = span.attr('data-course-id');
    var player = cyberplayer("playercontainer").setup({
        width: '100%',
        height: '100%',
        file: video_url,
        image: cover_url,
        autostart: false,
        stretching: "uniform",
        repeat: false,
        volume: 100,
        controls: true,
        // primary: 'flash', flash优先
        tokenEncrypt: "true",
        // AccessKey
        ak: '92166a15820c4d2eb7798a57ee8230d2'
    });
    player.on("beforePlay",function (e) {
        // 不是m3u8格式的就不是加密视频
        if(!/m3u8/.test(e.file)){
            return;
        }

        xfzajax.get({
            'url': '/course/course_token/',
            'data': {
                'video_url': video_url,
                'course_id': course_id
            },
            'success': function (result) {
                if(result['code'] === 200){
                    var token = result['data']['token'];
                    console.log('token:', token);
                    player.setToken(e.file,token);
                }else{
                    window.messageBox.showError(result.message);
                    player.stop()
                }
            }
        });
    });
});