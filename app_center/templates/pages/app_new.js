$(document).ready(function() {
	var status = $('.ui.form .ui.message');
	$('form').ajaxForm({
		beforeSend: function() {
			status.empty();
		},
		success: function() {
			status.html('Done!');
		},
		complete: function(xhr) {
		},
		error: function(xhr) {
			status.html(xhr.responseText);
		}
	});
});