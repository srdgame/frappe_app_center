$(document).ready(function() {
	var bar = $('.bar');
	var upload_form = $('.ui.upload_app.form');

	upload_form.form({
		fields: {
			app: 'empty',
			app_name: 'empty',
			version : 'integer',
			comment : ['minLength[10]', 'empty'],
			terms : 'checked'
		}
	});

	upload_form.ajaxForm({
		dataType: 'json',
		beforeSend: function() {
			upload_form.removeClass('success').removeClass('error');
		},
		uploadProgress: function(event, position, total, percentComplete) {
			var percentVal = percentComplete + '%';
			bar.width(percentVal);
		},
		success: function(response) {
			upload_form.find('.ui.success.message').html(response.message);
			upload_form.addClass('success');
			if( typeof on_upload_app_form_success === 'function' ){
				//存在且是function
				on_upload_app_form_success();
			}
		},
		complete: function(xhr) {
		},
		error: function(xhr) {
			console.log('Upload Exception:' + xhr.responseText);
			upload_form.addClass('error');
			upload_form.find('.ui.error.message').html(xhr.responseText);
			var _server_messages = JSON.parse(xhr.responseJSON._server_messages);
			upload_form.find('.ui.error.message').html(_server_messages[0]);
		}
	});
});