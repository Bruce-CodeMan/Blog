var PosterHandler = function () {
    var csrf_token = $("meta[name='csrf-token']").attr("content");
    var editor = new window.wangEditor("#editor");
    // 配置图片上传路径
    editor.config.uploadImgServer = "/poster/image/upload";
    editor.config.uploadFileName = "image";
    // csrf可以放到请求体中，也可以放到请求头中，先在请求体中寻找
    editor.config.uploadImgHeaders = {
        "X-CSRFToken": csrf_token
    }
    editor.create();
    this.editor = editor;
}

// 监听提交按钮
PosterHandler.prototype.listenSubmitEvent =function () {
    var that = this;
    $("#submit-btn").on("click", function (event){
        event.preventDefault();
        var title = $("input[name='title']").val();
        var board_id = $("select[name='board_id']").val();
        var content = that.editor.txt.html();
        bruce_ajax.post({
            url: "/poster/public",
            data: {
                title,
                board_id,
                content
            },
            success:function (result){
                if(result['code'] == 200) {
                    let data = result["data"]
                    let poster_id = data["poster_id"]
                    window.location.href="/poster/detail/" + poster_id
                }else{
                    alert(result["message"])
                }
            }
        })
    })
}

PosterHandler.prototype.run = function () {
    this.listenSubmitEvent();
}

$(function (){
    var poster = new PosterHandler();
    poster.run();
})