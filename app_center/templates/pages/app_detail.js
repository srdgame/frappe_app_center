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
			fork_app_form.find('.ui.error.message').html(xhr.responseText);
			console.log('Fork Application Exception:' + xhr.responseText);
			fork_app_form.find('.ui.error.message').html(xhr.responseJSON.exc);
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
	$('.ui.app.form .cancel.button').click(function(){
		$('.ui.upload_version.modal').modal('hide');
	});

	// For issue detail page
	$('.ui.feed .event .meta .fix').click(function () {
		$('.ui.issue_action.comment.form input[name="action"]').val("Closed");
		$('.ui.issue_action.modal .header').html('{{_("Issue fixed")}}');
		$('.ui.issue_action.modal')
			.modal({
				closable: true
			})
			.modal('show')
		;
	});
	$('.ui.feed .event .meta .invalid').click(function () {
		$('.ui.issue_action.comment.form input[name="action"]').val("Invalid");
		$('.ui.issue_action.modal .header').html('{{_("Invalid issue")}}');
		$('.ui.issue_action.modal')
			.modal({
				closable: true
			})
			.modal('show')
		;
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
			setTimeout(function() {
				window.location.reload(false);
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
});