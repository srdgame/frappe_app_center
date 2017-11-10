$(document).ready(function() {
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

	var descEditormdView = editormd.markdownToHTML("desc-editormd-view", {
		htmlDecode      : "style,script,iframe",  // you can filter tags decode
		emoji           : true,
		taskList        : true,
		tex             : true,  // 默认不解析
		flowChart       : true,  // 默认不解析
		sequenceDiagram : true,  // 默认不解析
	});
});