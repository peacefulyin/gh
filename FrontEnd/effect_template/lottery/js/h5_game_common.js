var $maskRule = $("#mask-rule"),//规则遮罩层
    $mask = $("#mask"),//红包遮罩层
	$mask2 = $("#mask2"),//红包遮罩层
	$mask3 = $("#mask3"),//红包遮罩层
    $winning = $(".winning"),//红包
    $card = $("#card"),
    $close = $("#close");
    //link = false;//判断是否在链接跳转中

//规则
$(".rule").click(function () {
    $maskRule.show();
});
$("#close-rule").click(function () {
    $maskRule.hide();
});

/*中奖信息提示*/
function win(f,l,a1) {
    //遮罩层显示
	var text=a1
    console.log('win');
    if(text==="谢谢参与~"){
		  $mask2.show();
	}else if (text === "服务器错误") {
        $mask3.show()
    } else {
        $("#text1").html(text);
        $('.scroll-ul').append("<li>恭喜<span class=\"start-num\">"+f+"</span>****<span class=\"end-num\">"+l+"</span>获得<span class=\"info\">"+text+"</span></li>")
        $("#txtMarqueeTop").slide({ mainCell:"ul",autoPlay:true,effect:"topMarquee",interTime:50,vis:6  })
        $mask.show();
    }
    $winning.addClass("reback");

	
    setTimeout(function () {
        $card.addClass("pull");
    }, 500);

    //关闭弹出层
    $("#close,.win,.btn").click(function () {
    //$close.click(function () {
        $mask.hide();
		 $mask2.hide();
        $mask3.hide()
        $winning.removeClass("reback");
        $card.removeClass("pull");
    });

}

//此处可以在commonjs中合并
function queryString(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(window.location.search);
    if(results === null) {
        return "";
    }
    else {
        return decodeURIComponent(results[1].replace(/\+/g, " "));
    }
}



