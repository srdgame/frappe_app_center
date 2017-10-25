$(document).ready(function() {
	$('.ui.app.upload.button').click(function () {
		var app = $(this).attr("app");
		alert("upload");
	});
	$('.ui.app.modify.button').click(function () {
		var app = $(this).attr("app");
		alert("modify");
	});
});

