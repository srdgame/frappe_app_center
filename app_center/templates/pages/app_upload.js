frappe.ready(function() {
	$.ajaxSetup({
		headers: { // 默认添加请求头
			"X-Frappe-CSRF-Token": frappe.csrf_token,
		}
	});
	$('form').ajaxForm({
		before_send: function() {
		},
		success: function() {
			alert('Success');
		},
		complete :function(xhr) {
			//alert('Done');
		},
		error: function(xhr) {
			if (xhr.responseJSON && xhr.responseJSON._server_messages) {
				msgs = JSON.parse(xhr.responseJSON._server_messages);
				alert(JSON.parse(msgs[0]).message);
			} else {
				alert("Error!");
			}
		}
	})();
});