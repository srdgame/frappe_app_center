$(document).ready(function() {
	var bar = $('.bar');

	$('.ui.app.form').form({
		fields: {
			app: 'empty',
			app_name: 'empty',
			version : 'integer',
			comment : ['minLength[10]', 'empty'],
			terms : 'checked'
		}
	});

	$('.ui.app.form').ajaxForm({
		dataType: 'json',
		beforeSend: function() {
			$('.ui.app.form').removeClass('success').removeClass('error');
		},
		uploadProgress: function(event, position, total, percentComplete) {
			var percentVal = percentComplete + '%';
			bar.width(percentVal);
		},
		success: function(response) {
			$('.ui.app.form .ui.success.message').html(response.message);
			$('.ui.app.form').addClass('success');
		},
		complete: function(xhr) {
		},
		error: function(xhr) {
			console.log('Upload Exception:' + xhr.responseText);
			$('.ui.app.form').addClass('error');
			$('.ui.app.form .ui.error.message').html(xhr.responseText);
			var _server_messages = JSON.parse(xhr.responseJSON._server_messages);
			$('.ui.app.form .ui.error.message').html(_server_messages[0]);
		}
	});
});