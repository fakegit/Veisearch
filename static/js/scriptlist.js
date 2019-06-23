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

    var test_id = window.location.href.substr(-2, 1);

    $(".like-btn").click(function () {
        $(".fa-thumbs-o-up").css("color", "#32CD32");
        $(".like-label").text("点赞+1")
    })

    $("#script-content").focus(function () {
        $("#script-content").hide();
        $(".form-data").show();
        $("#script-content-true").focus();
    });

    $("#script-test-btn").click(function () {
        $.ajax({
            url: "/script-test/" + test_id,
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
    });

    $("#comments-btn").click(function () {
        $.ajax({
            url: '/comments/' + test_id,
            async: false,
            type: 'POST',
            headers: {"Content-Type": "application/x-www-form-urlencoded"},
            data: {
                "comments_content": $("#script-content-true").val(),
                "comments_name": $("#comments_name").val(),
                "comments_email": $("#comments_email").val(),
            },
            dataType: "JSON",
            success: function (rep) {
                comments_img = rep.comments_img;
                comments_name = rep.comments_name;
                comments_content = rep.comments_content;
                add_time = rep.add_time;
                comments_nums = $(".script-comments-list .script-comments-detail").length + 1;

                new_comments_HTML = '<div class="script-comments-detail"><img src="/media/' + comments_img + '"/>' +
                    '<label class="script-comments-username">' + comments_name + '：</label>' +
                    '<label class="script-comments-detail-content">' + comments_content + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + add_time + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#' + comments_nums + '楼)</label> <hr align="center"/></div>'
                $(".script-comments-list").append(new_comments_HTML);
                $("#comments_name").val('');
                $("#comments_email").val('');
                $("#script-content-true").val('');
                $(".form-data").hide();
                $("#script-content").show();
                // <div class="script-comments-detail">
                //         <img src="/media/{{ comments.comments_img }}"/>
                //         <label class="script-comments-username">{{ comments.comments_name }}：</label>
                //         <label class="script-comments-detail-content">{{ comments.content }}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;({{ comments.add_time }}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#{{ forloop.counter }}楼)</label>
                //         <hr align="center"/>
                //     </div>
            }
        })
    })


});