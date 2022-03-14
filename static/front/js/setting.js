var SettingHandler = function () {}

// 监听上传头像的事件
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

// 监听提交的事件
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

// 监听近7天帖子数的事件
SettingHandler.prototype.listenPostersCountEvent = function (){
    bruce_ajax.get({
        url: "/day7/posters/count",
        success: function (res){
            if(res["code"] == 200){
                var poster_date = res["data"]["poster_date"]
                var poster_count = res["data"]["poster_count"]

                var line = new Morris.Line({
                element: 'line-chart',
                resize: true,
                data: [
                  {y: poster_date[Object.keys(poster_date)[0]], item1: poster_count[Object.keys(poster_count)[0]]},
                  {y: poster_date[Object.keys(poster_date)[1]], item1: poster_count[Object.keys(poster_count)[1]]},
                  {y: poster_date[Object.keys(poster_date)[2]], item1: poster_count[Object.keys(poster_count)[2]]},
                  {y: poster_date[Object.keys(poster_date)[3]], item1: poster_count[Object.keys(poster_count)[3]]},
                  {y: poster_date[Object.keys(poster_date)[4]], item1: poster_count[Object.keys(poster_count)[4]]},
                  {y: poster_date[Object.keys(poster_date)[5]], item1: poster_count[Object.keys(poster_count)[5]]},
                  {y: poster_date[Object.keys(poster_date)[6]], item1: poster_count[Object.keys(poster_count)[6]]}
                ],
                xkey: 'y',
                ykeys: ['item1'],
                labels: ['发帖子数'],
                lineColors: ['#efefef'],
                lineWidth: 2,
                hideHover: 'auto',
                gridTextColor: "#fff",
                gridStrokeWidth: 0.4,
                pointSize: 4,
                pointStrokeColors: ["#efefef"],
                gridLineColor: "#efefef",
                gridTextFamily: "Open Sans",
                gridTextSize: 10
              });
            }
        }
    })
}


SettingHandler.prototype.run = function () {
    this.listenAvatarUploadEvent();
    this.listenSubmitEvent();
    this.listenPostersCountEvent();
}

$(function (){
    var handler = new SettingHandler();
    handler.run();
});
