
$(document).ready(function() {
	$('.ui.feed .event .content .meta .reply').click(function(){
		$('.ui.comment.form textarea[name="comment"]').focus();
		$('html, body').animate({
			scrollTop: $('.ui.comment.form textarea[name="comment"]').offset().top
		}, 0);
	});
});