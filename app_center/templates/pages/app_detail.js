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
	$(".ui.button.fork").click(function () {
		window.location.href="/app_fork?app={{doc.name}}";
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