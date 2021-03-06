
function on_upload_app_form_success() {
	setTimeout(function () {
		window.location.href = window.location.pathname + "?app={{doc.name}}&tab=releases";
	}, 1000);
}

$(document).ready(function() {
	$('.ui.review.form .ui.star.rating')
		.rating({
			onRate: function(value) {
				var id = $(this).data('for');
				$('#'+id).val(value);
			}
		})
	;
	$('.comment .content .metadata .ui.star.rating')
	  .rating('disable')
	;
	$('.ui.feed .event .ui.star.rating')
	  .rating('disable')
	;
	$('.ui.comment.form').form({
		fields: {
			comment : ['minLength[15]', 'empty']
		}
	});

	$('.ui.review.form, .ui.issue.form').form({
		fields: {
			priority: 'empty',
			title : ['minLength[15]', 'empty'],
			content : ['minLength[50]', 'empty']
		}
	});

	//Tab page tab trigger functions
	$(".ui.tabular.menu .item").tab();

	$(".ui.button.edit").click(function () {
		window.location.href="/app_modify?app={{doc.name}}";
	});
	$(".ui.button.editor").click(function () {
		window.location.href="/app_editor?app={{doc.name}}";
	});
	$(".ui.button.follow").click(function () {
		//window.location.href="/app_modify?app={{doc.name}}";
	});
	$('.ui.button.fork_from').click(function(){
		window.location.href = "/app_detail?app={{doc.fork_from}}";
	});

{% if frappe.user != doc.owner %}
	$(".ui.button.fork").click(function () {
		$('.ui.fork_app.modal')
			.modal({
				closable  : false
			})
			.modal('show')
		;
	});
	$('.ui.fork_app.form .cancel.button').click(function(){
		$('.ui.fork_app.modal').modal('hide');
	});

	var fork_app_form = $('.ui.fork_app.form');
	fork_app_form.form({fields: { version : 'integer' }	});
	fork_app_form.ajaxForm({
		dataType: 'json',
		success: function (response) {
			fork_app_form.find('.ui.success.message').html("Fork application successfully!");
			fork_app_form.addClass('success');
			setTimeout(function () {
				window.location.href="/app_detail?app=" + response.message;
			}, 3000);
		},
		error: function(xhr) {
			fork_app_form.addClass('error');
			console.log('Fork Application Exception:' + xhr.responseText);
			if (xhr.responseJSON._server_messages) {
				fork_app_form.find('.ui.error.message').html(xhr.responseJSON._server_messages);
			} else {
				fork_app_form.find('.ui.error.message').html('Fork Application Failed!');
			}
		}
	});
{% else %}
	$(".ui.button.delete").click(function () {
		$('.ui.delete_app.modal')
			.modal({
				closable  : false
			})
			.modal('show')
		;
	});
	$('.ui.delete_app.form .cancel.button').click(function(){
		$('.ui.delete_app.modal').modal('hide');
	});

	var delete_app_form = $('.ui.delete_app.form');
	delete_app_form.form({fields: { version : 'integer' }	});
	delete_app_form.ajaxForm({
		dataType: 'json',
		success: function (response) {
			delete_app_form.find('.ui.success.message').html("Fork application successfully!");
			delete_app_form.addClass('success');
			setTimeout(function () {
				window.location.href="/app_detail?app=" + response.message;
			}, 3000);
		},
		error: function(xhr) {
			delete_app_form.addClass('error');
			delete_app_form.find('.ui.error.message').html(xhr.responseText);
			console.log('Fork Application Exception:' + xhr.responseText);
			delete_app_form.find('.ui.error.message').html(xhr.responseJSON.exc);
		}
	});

	$(".ui.button.upload").click(function () {
		$('.ui.upload_version.modal')
			.modal({
				closable  : false
			})
			.modal('show')
		;
	});
	$('.ui.upload_app.form .cancel.button').click(function(){
		$('.ui.upload_version.modal').modal('hide');
	});

{% endif %}
	var descEditormdViewObj = $('#desc-editormd-view');
	if (descEditormdViewObj.length > 0) {
		var descEditormdView = editormd.markdownToHTML("desc-editormd-view", {
			htmlDecode: "style,script,iframe",  // you can filter tags decode
			emoji: true,
			taskList: true,
			tex: true,  // 默认不解析
			flowChart: true,  // 默认不解析
			sequenceDiagram: true,  // 默认不解析
		});
	}

	$('.ui.review.form, .ui.comment.form, .ui.issue.form').ajaxForm({
		dataType: 'json',
		resetForm: true,
		beforeSend: function() {
			console.log('Ajax Form Before Send!');
		},
		success: function(response, status, xhr, form) {
			form.find('.ui.success.message').html('Done!');
			form.addClass('success');
			var tab = $(".ui.tabular.menu .active.item").data("tab");
			setTimeout(function() {
				if (tab && tab != 'undefined') {
					window.location.href = window.location.pathname + "?app={{doc.name}}&tab=" + tab;
				} else {
					window.location.reload(false);
				}
			}, 1000);
		},
		complete: function(xhr) {
		},
		error: function(xhr, status, error, form) {
			console.log('Form Exception:' + xhr.responseText);
			form.addClass('error');
			form.find('.ui.error.message').html(xhr.responseText);
			if (xhr.responseJSON._server_messages) {
				var _server_messages = JSON.parse(xhr.responseJSON._server_messages);
				form.find('.ui.error.message').html(_server_messages[0]);
			} else {
				var exc = JSON.parse(xhr.responseJSON.exc);
				form.find('.ui.error.message').html(exc);
			}
		}
	});


	$(".ui.feed .event .content .meta .delete").click(function () {
		var name = $(this).data("name");
		var type = $(this).data("type");
		$('.ui.delete_confirm.modal')
			.modal({
				closable  : false,
				onApprove : function() {
					var url = "/api/method/app_center.appmgr.remove_" + type;
					$.ajax({
						type: "POST",
						url: url,
						data: {"name": name},
						dataType: "json",
						success: function (data, status, xhr) {
							console.log(data);
							window.location.href="/app_detail?app={{doc.name}}&tab=" + type + "s";
						},
						error: function (xhr, status, error ) {
							console.log(xhr.responseText);
							$('.ui.comment.form').addClass('error');
							$('.ui.comment.form .ui.error.message').html(xhr.responseJSON);
						}
					});
				}
			})
			.modal('show')
		;
	});
	$('.ui.comments .comment .content .actions .delete').click(function() {
		var name = $(this).data("name");
		var type = $(this).data("type");
		var parent = $(this).data("parent");
		var tab = $(".ui.tabular.menu .active.item").data("tab");
		$('.ui.delete_comment.modal')
			.modal({
				closable  : false,
				onApprove : function() {
					var url = "/api/method/app_center.appmgr.remove_comment";
					if (type && type != 'undefined') {
						url = "/api/method/app_center.appmgr.remove_" + type + "_comment";
					}
					$.ajax({
						type: "POST",
						url: url,
						data: {"parent": parent, "name": name},
						dataType: "json",
						success: function (data, status, xhr) {
							console.log(data);
							if (tab && tab != 'undefined') {
								window.location.href = window.location.pathname + "?app={{doc.name}}&tab=" + tab;
							} else {
								window.location.reload(false);
							}
						},
						error: function (xhr, status, error ) {
							console.log(xhr.responseText);
							$('.ui.comment.form').addClass('error');
							$('.ui.comment.form .ui.error.message').html(xhr.responseJSON);
						}
					});
				}
			})
			.modal('show')
		;
	});
	$('.ui.comments .comment .content .actions .install').click(function() {
		var app =  $(this).data('app');
		var version = $(this).data('version');
		// Show device list then apply installation to selected device
		//window.open("/files/app_center_files/" + app + "/" + version + ".zip");
	});
	$('.ui.comments .comment .content .actions .fork').click(function() {
		var version = $(this).data('version');
		$('.ui.fork_app.form input[name="version"]').val(version);
		$('.ui.fork_app.modal')
			.modal({
				closable  : false
			})
			.modal('show')
		;
	});
	$('.ui.comments .comment .content .actions .reply').click(function(){
		var reply_name = $(this).data('name');
		var reply_user = $(this).data('user');
		$('.ui.comment.form input[name="reply_to"]').val(reply_name);
		$('.ui.comment.form input[name="reply_to_user"]').val(reply_user);
		$('.ui.comment.form textarea[name="comment"]').focus();
		$('html, body').animate({
			scrollTop: $('.ui.comment.form textarea[name="comment"]').offset().top
		}, 0);
	});
});