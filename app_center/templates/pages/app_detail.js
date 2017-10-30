$(document).ready(function() {
	//Tab page tab trigger functions

	$(".menu .item").tab();
	$('#context1 .menu .item').tab({
		context: $('#context1')
	});
	$('.paths.example .menu .item').tab({
		context: '.paths.example'
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