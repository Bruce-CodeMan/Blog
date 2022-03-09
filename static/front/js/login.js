var LoginHandler = function () {}

// 监听登录
LoginHandler.prototype.listenSubmitEvent = function () {
    $('#submit-btn').on("click", function (event){
        event.preventDefault();
        var email = $("input[name='email']").val();
        var password = $("input[name='password']").val();
        var remember_me = $("input[name='remember']").prop("checked");
        bruce_ajax.post({
            url:'/login',
            data:{
                email,
                password,
                remember_me: remember_me?1:0
            },
            success:function (result) {
                if(result['code'] == 200) {
                    // 获取token
                    var token = result["data"]["token"]
                    var user = result["data"]["user"]
                    localStorage.setItem("JWT_TOKEN_KEY", token)
                    localStorage.setItem("USER_KEY", JSON.stringify(user))
                    window.location.href = "/"
                }else {
                    alert(result['message']);
                }
            }
        })
    })
}

LoginHandler.prototype.run = function () {
    this.listenSubmitEvent();
}

$(function (){
   var handler = new LoginHandler();
   handler.run();
});