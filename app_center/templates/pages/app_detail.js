$(document).ready(function() {
	//Tab page tab trigger functions
	$(".main.container .tabular.menu .item").tab();

	var descEditormdView = editormd.markdownToHTML("desc-editormd-view", {
		htmlDecode      : "style,script,iframe",  // you can filter tags decode
		emoji           : true,
		taskList        : true,
		tex             : true,  // 默认不解析
		flowChart       : true,  // 默认不解析
		sequenceDiagram : true,  // 默认不解析
	});
});