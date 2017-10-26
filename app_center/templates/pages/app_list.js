$(document).ready(function() {
	$('.ui.app-upload.button').click(function () {
		var app = $(this).attr("app");
		window.location.href="/app_upload?app="+app;
	});
	$('.ui.app-modify.button').click(function () {
		var app = $(this).attr("app");
		window.location.href="/app_modify?app="+app;
	});
	$('.ui.app-add.button').click(function () {
		window.location.href="/app_new";
	});
});

