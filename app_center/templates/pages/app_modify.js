$(document).ready(function() {
	var status = $('.ui.form .ui.message');
	$('form').ajaxForm({
		beforeSend: function() {
			status.empty();
		},
		success: function() {
		},
		complete: function(xhr) {
			status.html('<br>'+xhr.responseText);
		},
		error: function(xhr) {
			status.html(xhr.responseText);
		}
	});
});