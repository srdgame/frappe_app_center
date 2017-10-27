function jsonToQueryString(json) {
    return '?' +
        Object.keys(json).map(function(key) {
            return encodeURIComponent(key) + '=' +
                encodeURIComponent(json[key]);
        }).join('&');
};

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
	$('.ui.app-refresh.button').click(function () {
		var category = $('#category_filter .menu .item.selected').attr("value");
		if (category != null) {
			window.location.href="/app_list"+jsonToQueryString({"category":category});
		} else {
			window.location.href = "/app_list";
		}
	});
	$('.ui.app-clean.button').click(function () {
		window.location.href="/app_list";
	});
});

