$(function () {
    var nav = $(".head"); //导航，请自行修改
    var maxTop = 60; //高度，请自行修改
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

        $(".btn1").addClass("active");

        $(".type-btn").click(function () {
            $(".type-btn").removeClass("active");
            $(".data-format").removeClass("active");
            // $(this).addClass("active");
            $("." + $(this).attr("class").substring(9, 13)).addClass("active");

        });
        $(".script-files").change(function () {
            var file = $(".script-files")[0].files[0];
            var reader = new FileReader;
            reader.readAsText(file, 'utf-8');
            reader.onload = function (evt) {
                var data = evt.target.result;
                $('code.python').text(data);
            };
            $("form.upload-script fieldset").addClass("active");
        });
        $("#vercode-img").css('cursor', 'pointer').click(function () {
            $(this)[0].src += Math.random();
        });
        $("#submit-btn").click(function () {

            var requird = true;
            $(".requird").each(function () {
                var val = $.trim($(this).val());
                if (val == '') {
                    $(this).focus();
                    shake($(this), "selectshake", 4);
                    requird = false;
                    return false;
                }
            });
            if (requird === true) {
                var script_file = document.getElementById("script-file").files[0];
                var script_type = $("#script-type option:selected").val();
                var website_address = $("#website_address").val();
                var website_img = document.getElementById("website_img").files[0];
                var website_name = $("#website_name").val();
                var author = $("#author").val();
                var author_email = $("#author_email").val();
                var checkbox = $("#checkbox").prop("checked");
                var function_introduce = $("#function_introduce").val();
                var vercode = $("#vercode-content").val();
                var formdata = new FormData();
                formdata.append("script_file", script_file);
                formdata.append("script_type", script_type);
                formdata.append("website_address", website_address);
                formdata.append("website_img", website_img);
                formdata.append("website_name", website_name);
                formdata.append("author", author);
                formdata.append("author_email", author_email);
                formdata.append("checkbox",checkbox);
                formdata.append("function_introduce", function_introduce);
                formdata.append("vercode", vercode);
                $.ajax({
                    url: "/upload/",
                    async: false,
                    type: 'POST',
                    data: formdata,
                    processData: false, //告诉jQuery不要去处理发送的数据
                    contentType: false, //告诉jQuery不要去设置Content-Type请求头
                    success:
                        function (arg) {
                           if (arg == "False"){
                               $("#vercode-error").hide();
                               $("#submit-btn").after('<label id="vercode-error" style="color: #FF0000;margin-left: 30px">验证码输入错误！</label>')
                           }
                           else {
                               window.location.href = "/upload-success/"
                           }
                        }
                })
                ;
            } else {
                return false;
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


    }
);
