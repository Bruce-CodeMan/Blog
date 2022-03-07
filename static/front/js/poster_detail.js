$(function (){
    // 初始化代码高亮
    hljs.highlightAll();
    // 评论按钮
    $("#comment-btn").on("click", function (event){
        var $this = $(this);
        event.preventDefault();
        var content =$("#comment-textarea").val();
        var poster_id = $this.attr("data-poster-id");
        var user_id = $this.attr("data-user-id");
        if(!user_id || user_id == "") {
            window.location.href="/login"
            return
        }
        bruce_ajax.post({
            url:"/comment",
            data: {
                content,
                poster_id
            },
            success:function (result){
                if(result['code']==200){
                    window.location.reload();
                }else{
                    alert(result["message"])
                }
            }
        })
    })
})