$(function() {
	var nav = $(".head"); //导航，请自行修改
	var maxTop = 60; //高度，请自行修改
	$(window).on('scroll', function() {
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
$(document).ready(function() {

	$(".btn1").addClass("active");

	$(".type-btn").click(function() {
		$(".type-btn").removeClass("active");
		$(".data-format").removeClass("active");
		// $(this).addClass("active");
		$("."+$(this).attr("class").substring(9,13)).addClass("active");

	})
	$(".script-files").change(function(){
		var file = $(".script-files")[0].files[0];
		var reader = new FileReader;
		reader.readAsText(file,'utf-8');
		reader.onload = function(evt){
			var data = evt.target.result;
			$('code.python').text(data);
		}
		$("form.upload-script fieldset").addClass("active");
	})

})
