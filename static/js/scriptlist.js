$(function(){
    var nav = $(".head");   //导航，请自行修改
    var maxTop = 60;      //高度，请自行修改
    $(window).on('scroll',function(){
        var top = $(window).scrollTop();
        if (top > maxTop) {
            nav.css({
                'position':'fixed',
                'top':0
            });
        }
        if (top < maxTop) {
            nav.css('position','relative');
        }
    });
	
});
$(document).ready(function(){
	$(".like-btn").click(function(){
		$(".fa-thumbs-o-up").css("color","#32CD32");
		$(".like-label").text("点赞+1")
	})
	
	$("#script-content").focus(function(){
		$("#script-content").hide();
		$(".form-data").show();
		$("#script-content-true").focus();
	})
})