//validation settings in formvalidation page
'use strict'

$(document).ready(function() {
	$('.ui.form').form({
		fields: {
		  app_name : 'empty',
		  category : 'empty',
		  protocol : 'empty',
		  device_supplier : 'empty',
		  device_serial : ['minLength[3]', 'empty'],
		  terms : 'checked'
		}
	});

	$('.ui.form').ajaxForm({
		beforeSend: function() {
		},
		success: function(response) {
			var action = $('.ui.form .ui.submit.button').text();
			$('.ui.form .ui.success.message').html('Application ' + response.message.name + ' ' + action + '!');
			$('.ui.form').addClass('success');
		},
		complete: function(xhr) {
		},
		error: function(xhr) {
			$('.ui.form .ui.error.message').html(xhr.responseText);
			$('.ui.form').addClass('error');
		}
	});
});