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
	$('form').submit(function() {
		// submit the form
		contentType: "application/x-www-form-urlencoded; charset=utf-8",
		$(this).ajaxSubmit();
		// return false to prevent normal browser submit and page navigation
		return false;
	});
});