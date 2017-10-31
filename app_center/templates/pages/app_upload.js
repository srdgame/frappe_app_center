$(document).ready(function() {
	var status = $('.ui.form .ui.message');
	var bar = $('.bar');

	$('.ui.app.form').form({
		fields: {
		  version : 'empty',
		  comments : ['minLength[10]', 'empty'],
		  terms : 'checked'
		}
	});

	$('form').ajaxForm({
		beforeSend: function() {
			status.empty();
		},
		uploadProgress: function(event, position, total, percentComplete) {
			var percentVal = percentComplete + '%';
			bar.width(percentVal);
			status.text(percentVal);
		},
		success: function() {
			var percentVal = '100%';
			bar.width(percentVal);
			status.text(percentVal);
		},
		complete: function(xhr) {
			status.html('<br>'+xhr.responseText);
		},
		error: function(xhr) {
			status.html(xhr.responseText);
		}
	});
});