function binCaptchaBtnClick() {
    $("#captcha-btn").on("click", function (event) {
        var email = $("input[name='email']").val();
        var $this=$(this)
        if (!email) {
            alert("请先输入邮箱!")
            return;
        }
        $.ajax({
            url:"/user/captcha",
            method:"POST",
            data:{
                "email":email
            },
            success:function (res){
                var code=res["code"];
                if(code===200){
                    //取消点击事件
                    $this.off("click");
                    var countDown=60;
                    var timer=setInterval(function (){
                        countDown-=1;
                        if (countDown>0){
                            $this.text(countDown+"秒后重新发送");
                        }else {
                            $this.text("获取验证码");
                            //重新执行函数
                            binCaptchaBtnClick();
                            //清除倒计时
                            clearInterval(timer)
                        }

                    },1000);
                    alert("验证码发送成功!")
                }else {
                    alert(res["message"])
                }
            }

        })

    });
}

// 等数据全部加载之后开始执行
$(function () {
    binCaptchaBtnClick();
});