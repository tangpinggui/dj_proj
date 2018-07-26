$(function () {
   var clearBtn = $('.clear-btn');
   clearBtn.click(function () {
       alert('start');
       xfzajax.post({
           'url': 'http://192.168.0.121:8000/loginFaceName/',
           'data': {
               'faceCode': '111111'
           },
           'success': function (result) {
               alert(111111111111111111);
               console.log(result);
               // if(result['status'] === 0)
               // console.log(result)
           },
           'fail': function (result) {
               alert('??????')
           }
       })
   })
});