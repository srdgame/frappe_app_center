//validation settings in formvalidation page
'use strict'
$(document).ready(function() {
	$('.ui.app.form').form({
		fields: {
		  app_name : 'empty',
		  category : 'empty',
		  protocol : 'empty',
		  device_supplier : 'empty',
		  device_serial : ['minLength[3]', 'empty'],
		  terms : 'checked'
		}
	});

	$('.ui.app.form').ajaxForm({
		beforeSend: function() {
		},
		success: function(response) {
			var action = $('.ui.form .ui.submit.button').text();
			$('.ui.app.form .ui.success.message').html('Done!');
			$('.ui.app.form').addClass('success');
			setTimeout(function() {
				window.location.href = "/app_list";
			}, 2000);
		},
		complete: function(xhr) {
		},
		error: function(xhr) {
			$('.ui.app.form .ui.error.message').html(xhr.responseText);
			$('.ui.app.form').addClass('error');
		}
	});
});
