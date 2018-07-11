
// 点击切换图形验证码
$(function () {
    var imgCaptcha = $('.img-captcha');
    imgCaptcha.click(function () {
        imgCaptcha.attr("src",'/account/register/img/captcha'+"?random="+Math.random());
    });
});


// 点击发送短信验证码
$(function () {
    var smsCaptcha = $('.sms-captcha-btn');
    function send_sms() {
        // 获取手机号码的时候，获取的是手机号码，而不是手机号码的输入框
        var telephone = $('input[name="telephone"]').val();
        console.log(telephone);
        $.get({
            'url': '/account/register/sms/captcha/',
            'data':{'telephone': telephone},
            'success': function (result) {
                var count = 10;
                smsCaptcha.addClass('disabled');
                smsCaptcha.unbind('click');
                var timer = setInterval(function () {
                    smsCaptcha.text(count);
                    count--;
                    if(count <= 0){
                        clearInterval(timer);
                        smsCaptcha.text('发送验证码');
                        smsCaptcha.removeClass('disabled');
                        smsCaptcha.click(send_sms);
                    }
                },1000);
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    }
    smsCaptcha.click(send_sms);
});


// 注册功能
$(function () {
    var telephoneInput = $("input[name='telephone']");
    var usernameInput = $("input[name='username']");
    var imgCaptchaInput = $("input[name='img_captcha']");
    var password1Input = $("input[name='password1']");
    var password2Input = $("input[name='password2']");
    var smsCaptchaInput = $("input[name='sms_captcha']");
    var submitBtn = $(".submit-btn");

    submitBtn.click(function (event) {
        // 禁止掉传统的表单发送数据的方式
       event.preventDefault();

       var telephone = telephoneInput.val();
       var username = usernameInput.val();
       var imgCaptcha = imgCaptchaInput.val();
       var password1 = password1Input.val();
       var password2 = password2Input.val();
       var smsCaptcha = smsCaptchaInput.val();
       console.log(telephone,username,imgCaptcha)
       if(!telephone||telephone.length != 11){
           alert('手机号码输入不正确！');
           return;
        }

        xfzajax.post({
            'url': '/account/register/',
            'data': {
                'telephone': telephone,
                'username': username,
                'img_auth': imgCaptcha,
                'password': password1,
                'password1': password2,
                'short_auth': smsCaptcha
            },
            'success': function (result) {
                if(result['code'] === 200){
                    window.location = '/';
                }else{
                    var message = result['message'];
                    window.messageBox.showError(message);
                }
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    });
});