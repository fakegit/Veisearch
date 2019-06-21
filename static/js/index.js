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