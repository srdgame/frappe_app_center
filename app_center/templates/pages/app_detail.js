$(document).ready(function() {
	$('.ui.comment.form').form({
		fields: {
		  comment : ['minLength[15]', 'empty']
		}
	});

	$('.ui.review.form, .ui.issue.form').form({
		fields: {
		  title : ['minLength[6]', 'empty'],
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
			fork_app_form.find('.ui.error.message').html(xhr.responseText);
			console.log('Fork Application Exception:' + xhr.responseText);
			fork_app_form.find('.ui.error.message').html(xhr.responseJSON.exc);
			fork_app_form.addClass('error');
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
			delete_app_form.find('.ui.error.message').html(xhr.responseText);
			console.log('Fork Application Exception:' + xhr.responseText);
			delete_app_form.find('.ui.error.message').html(xhr.responseJSON.exc);
			delete_app_form.addClass('error');
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
{% endif %}

	var descEditormdView = editormd.markdownToHTML("desc-editormd-view", {
		htmlDecode      : "style,script,iframe",  // you can filter tags decode
		emoji           : true,
		taskList        : true,
		tex             : true,  // 默认不解析
		flowChart       : true,  // 默认不解析
		sequenceDiagram : true,  // 默认不解析
	});

	$('.ui.review.form, .ui.comment.form').ajaxForm({
		dataType: 'json',
		beforeSend: function() {
		},
		success: function(response) {
			$(this).find('.ui.success.message').html('Done!');
			$(this).addClass('success');
			window.location.href = "#"
		},
		complete: function(xhr) {
		},
		error: function(xhr) {
			console.log('Form Exception:' + xhr.responseText);
			$(this).find('.ui.error.message').html(xhr.responseText);
			var _server_messages = JSON.parse(xhr.responseJSON._server_messages);
			$(this).find('.ui.error.message').html(_server_messages[0]);
			$(this).addClass('error');
		}
	});
});