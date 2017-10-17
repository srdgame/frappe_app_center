frappe.ready(function() {
	$.ajaxSetup({
		headers: { // 默认添加请求头
			"X-Frappe-CSRF-Token": frappe.csrf_token
		}
	});
	$('form').ajaxForm({
		before_send: function() {
		},
		success: function(xhr) {
			frappe.msgprint(xhr.message);
		},
		complete :function(xhr) {
			//frappe.msgprint('Done');
		},
		error: function(xhr) {
			if (xhr.responseJSON && xhr.responseJSON._server_messages) {
				msgs = JSON.parse(xhr.responseJSON._server_messages);
				frappe.msgprint(JSON.parse(msgs[0]).message);
			} else {
				frappe.msgprint("Error!");
			}
		}
	})();
});