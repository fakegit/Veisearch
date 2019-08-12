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

    var test_id = window.location.href.split('/')[4];

    $(".like-btn").click(function () {
        // $(".fa-thumbs-o-up").css("color", "#32CD32");
        // $(".like-label").text("点赞+1");
        $.ajax({
            url: "/like/" + test_id + "/",
            async: false,
            type: "POST",
            headers: {"Content-Type": "application/x-www-form-urlencoded"},
            success: function (arg) {
                if (arg == "like_True") {
                    $(".fa-thumbs-o-up").css("color", "#32CD32");
                    $(".like-label").text("点赞+1");
                }
            }
        })
    })

    $("#script-content").focus(function () {
        $("#script-content").hide();
        $(".form-data").show();
        $("#script-content-true").focus();
    });

    $("#script-test-btn").click(function () {
        alert(test_id);
        var val = $.trim($("#wd").val());
        if (val == '') {
            $("#wd").focus();
            shake($("#wd"), "selectshake", 4);
        }
        else {
            $.ajax({
                url: "/script-test/" + test_id + '/',
                async: false,
                type: 'POST',
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                data: {
                    "wd": $("#wd").val(),
                },
                dataType: "JSON",
                success: function (arg) {
                    $('#test-result').text(arg);
                    $(".script-result").show();
                }
            });


        }

    });

    function shake(ele, cls, times) {//边框闪烁
        var i = 0, t = false, o = ele.attr("class") + " ", c = "", times = times || 2;
        if (t) return;
        t = setInterval(function () {
            i++;
            c = i % 2 ? o + cls : o;
            ele.attr("class", c);
            if (i == 2 * times) {
                clearInterval(t);
                ele.removeClass(cls);
            }
        }, 200);
    };

    $("#comments-btn").click(function () {

        var requird = true;
            $(".required").each(function () {
                var val = $.trim($(this).val());
                if (val == '') {
                    $(this).focus();
                    shake($(this), "selectshake", 4);
                    requird = false;
                    return false;
                }
            });
            if (requird === true) {
                $.ajax({
            url: '/comments/' + test_id + '/',
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
            }
        });
            }else {
                return false;
            }





    })


});