
$(document).ready(function() {
	$('.ui.feed .event .content .meta .reply').click(function(){
		$('.ui.comment.form input[name="comment"]').focus();
	});
});