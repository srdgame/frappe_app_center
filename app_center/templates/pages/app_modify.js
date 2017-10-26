$(document).ready(function() {
	$.ajaxSetup({
		headers: { // 默认添加请求头
			"X-Frappe-CSRF-Token": frappe.csrf_token
		}
	});
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