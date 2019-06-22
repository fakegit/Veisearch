$(function () {
    var nav = $(".head");   //导航，请自行修改
    var maxTop = 60;      //高度，请自行修改
    $(window).on('scroll', function () {
        var top = $(window).scrollTop();
        if (top > maxTop) {
            nav.css({
                'position': 'fixed',
                'top': 0
            });
        }
        if (top < maxTop) {
            nav.css('position', 'relative');
        }
    });

});
$(document).ready(function () {
    $(".like-btn").click(function () {
        $(".fa-thumbs-o-up").css("color", "#32CD32");
        $(".like-label").text("点赞+1")
    })

    $("#script-content").focus(function () {
        $("#script-content").hide();
        $(".form-data").show();
        $("#script-content-true").focus();
    })

    var test_id = window.location.href.substr(-2,1)
    $(document).ready(function () {
        $("#script-test-btn").click(function () {
            $.ajax({
                url: "/script-test/"+test_id,
                async: false,
                type: 'POST',
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                data: {
                    "wd": $("#wd").val(),
                },
                dataType: "JSON",
                success: function (arg) {
                    $('#test-result').text(arg)
                }
            });

            $(".script-result").show();
        })
    })
})