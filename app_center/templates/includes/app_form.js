//validation settings in formvalidation page
'use strict'

$(document).ready(function() {
	$('.ui.form').form({
		fields: {
			app_name: {
				identifier: 'app_name',
				rules: [{
					type: 'empty',
					prompt: 'Please enter application name'
				}]
			},
			category: {
				identifier: 'category',
				rules: [{
					type: 'empty',
					prompt: 'Please select application category'
				}]
			},
			protocol: {
				identifier: 'protocol',
				rules: [{
					type: 'empty',
					prompt: 'Please select application protocol'
				}]
			},
			device_supplier: {
				identifier: 'device_supplier',
				rules: [{
					type: 'empty',
					prompt: 'Please select application device_supplier'
				}]
			},
			device_serial: {
				identifier: 'device_serial',
				rules: [{
					type: 'empty',
					prompt: 'Please select application device_serial'
				}, {
					type: 'minLength[3]',
					prompt: 'Your password must be at least {ruleValue} characters'
				}]
			},
			terms: {
				identifier: 'terms',
				rules: [{
					type: 'checked',
					prompt: 'You must agree to the terms and conditions'
				}]
			}
		}
	});

	$('form').ajaxForm({
		beforeSend: function() {
		},
		success: function() {
			$('.ui.form .ui.success.message').html('<br>'+xhr.responseText);
		},
		complete: function(xhr) {
		},
		error: function(xhr) {
			$('.ui.form .ui.error.message').html(xhr.responseText);
		}
	});
});