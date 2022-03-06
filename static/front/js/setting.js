var SettingHandler = function () {}

SettingHandler.prototype.listenAvatarUploadEvent = function () {
    $("#avatar-input").on("change", function (){
        var image = this.files[0];
        var formData = new FormData();
        formData.append("image", image);
        bruce_ajax.post({
            url: "/avatar/upload",
            data: formData,
            // 使用jquery上传需要指定以下两个参数
            processData:false,
            contentType:false,
            success:function (result) {
                if(result['code']==200){
                    var avatar = result['data']['avatar'];
                    var avatar_url = "/media/avatar/" + avatar;
                    $("#avatar-img").attr("src", avatar_url);
                }
            }
        })
    })
}

SettingHandler.prototype.listenSubmitEvent = function () {
    $("#submit-btn").on("click", function (event){
        event.preventDefault();
        var signature = $('#signature-input').val();
        if(!signature){
            alert("提交成功");
            return;
        }
        if(signature && (signature.length>50 || signature.length<2)){
            alert("签名长度不正确");
            return;
        }
        bruce_ajax.post({
            url:"/profile/edit",
            data:{signature},
            success:function (result){
                if(result['code']==200){
                    alert('提交成功')
                }else{
                    alert(result['message'])
                }
            }
        })
    })
}

SettingHandler.prototype.run = function () {
    this.listenAvatarUploadEvent();
    this.listenSubmitEvent();
}

$(function (){
    var handler = new SettingHandler();
    handler.run();
});
