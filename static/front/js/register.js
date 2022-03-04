/**
 * Created by Bruce on 2022/3/5.
 */

var RegisterHandler = function(){

}

// 监听邮箱验证码
RegisterHandler.prototype.listenSendCaptureEvent = function (){
    var callback = function (event) {
        // 原生js对象转成jquery对象
        $this = $(this);
        //阻止默认的点击事件
        event.preventDefault();
        //邮箱的正则表达式
        var reg = /^\w+((.\w+)|(-\w+))@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+).[A-Za-z0-9]+$/;
        var email = $("input[name='email']").val();
        if (!email || !reg.test(email)) {
            alert("请输入正确格式的邮箱！")
            return
        }
        zlajax.get({
            url: "/email/capture?email=" + email,
            success: function (result) {
                if (result["code"] == 200) {
                    // 取消按钮的点击事件
                    $this.off("click");
                    // 添加禁用状态
                    $this.attr("disabled", "disabled");
                    // 开始倒计时
                    var countDown = 10;
                    var interval = setInterval(function () {
                        if (countDown > 0) {
                            $this.text("重新发送(" + countDown + "s)");
                        } else {
                            $this.text("发送验证码");
                            $this.attr("disabled", false);
                            $this.on("click", callback);
                            clearInterval(interval);
                        }
                        countDown--;

                    }, 1000);
                }
            }
        })
    };
    $("#email-captcha-btn").on("click", callback);
}

// 监听图片验证码
RegisterHandler.prototype.listenGraphCaptchaEvent = function (){
    $('#captcha-img').on("click", function (){
        var $this = $(this);
        var src = $this.attr("src");
        // 重新设置src属性
        // 如果是老的浏览器，相同的请求是不会再次请求后端的
        // graph/captcha?sign=Math.random()
        let newSrc = zlparam.setParam(src, "sign", Math.random())
        $this.attr("src", newSrc)
    })
}

RegisterHandler.prototype.run = function (){
    this.listenSendCaptureEvent();
    this.listenGraphCaptchaEvent();
}

// 等整个页面加载完成在执行js文件
$(function(){
    var handler = new RegisterHandler();
    handler.run();
})