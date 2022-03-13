/**
 * Created by Bruce on 2022/3/13.
 */


var PasswordHandler = function (){}

PasswordHandler.prototype.listenSendCaptureEvent = function (){
    var callback = function (event){
        // 原生js对象转成jquery对象
        $this = $(this);
        // 阻止默认的点击事件
        event.preventDefault();
        // 邮箱的正则表达式
        var reg = /^\w+((.\w+)|(-\w+))@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+).[A-Za-z0-9]+$/;
        var email = $("input[name='email']").val();
        if(!email || !reg.test(email)){
            alert("请输入正确格式的邮箱")
            return
        }

        bruce_ajax.get({
            url: "/email/capture?email=" + email,

            success: function (result) {
                if(result['code'] == 200){
                    // 取消按钮的点击事件
                    $this.off("click");
                    // 添加禁用状态
                    $this.attr("disabled", "disabled");
                    // 开始倒计时
                    var countdown = 300;
                    var interval = setInterval(function (){
                        if(countdown > 0){
                            $this.text("重新发送(" + countdown +"s)");
                        }else {
                            $this.text("发送验证码");
                            $this.attr("disabled", false);
                            $this.on("click", callback);
                            clearInterval(interval)
                        }
                        countdown--;
                    }, 1000);
                }
            }
        })
    };
    $("#email-captcha-btn").on("click", callback);
}

// 监听图片验证码
PasswordHandler.prototype.listenGraphCaptchaEvent = function (){
    $("#captcha-img").on("click", function (){
        var $this = $(this);
        var src = $this.attr("src");
        let newSrc = bruce_param.setParam(src, "sign", Math.random())
        $this.attr("src", newSrc)
    })
}

// 监听修改密码的按钮
PasswordHandler.prototype.listenSubmitEvent = function (){
    $("#reset_btn").on("click", function (event){
        event.preventDefault();
        var email = $("input[name='email']").val();
        var email_captcha = $("input[name='email_captcha']").val();
        var password = $("input[name='password']").val();
        var repeat_password = $("input[name='reset_password']").val();
        var graph_captcha = $("input[name='graph_captcha']").val();
        console.log(graph_captcha)
        bruce_ajax.post({
            url: "/password",
            data: {
                email,
                email_captcha,
                password,
                repeat_password,
                graph_captcha
            },
            success: function (result){
                if(result["code"] == 200) {
                    window.location = "/login"
                }else {
                    alert(result["message"])
                }
            }
        })
    })
}

PasswordHandler.prototype.run = function (){
    this.listenGraphCaptchaEvent();
    this.listenSendCaptureEvent();
    this.listenSubmitEvent();
}

$(function (){
    var handler = new PasswordHandler();
    handler.run();
})