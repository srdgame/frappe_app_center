function jsonToQueryString(json) {
    return '?' +
        Object.keys(json).map(function(key) {
            return encodeURIComponent(key) + '=' +
                encodeURIComponent(json[key]);
        }).join('&');
};

function on_upload_app_form_success() {
	setTimeout(function () {
		$('.ui.upload_version.modal').modal('hide');
	}, 1000);
};

$(document).ready(function() {
	$('.ui.items .item .content .meta .ui.star.rating')
	  .rating('disable')
	;
	$('.ui.items .item .content .extra .upload').click(function () {
		var app = $(this).data("name");
		var upload_form = $('.ui.upload_version.modal .ui.upload_app.form');
		upload_form.resetForm();
		upload_form.find('input[name="app"]').val(app);
		$('.ui.upload_version.modal')
			.modal({
				closable  : false
			})
			.modal('show')
		;
	});
	$('.ui.upload_version.modal .ui.upload_app.form .cancel.button').click(function(){
		$('.ui.upload_version.modal').modal('hide');
	});

	$('.ui.items .item .content .extra .modify').click(function () {
		var app = $(this).data("name");
		window.location.href="/app_modify?app="+app;
	});
	$('.ui.items .item .content .extra .comment').click(function() {
		var app = $(this).data("name");
		window.location.href="/app_detail?app="+app+"&tab=comments";
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
		//window.location.href="/app_list";
		$('#category_filter .text').text('{{_("Category Filter")}}');
		$('#category_filter .menu .item.selected').removeClass("active selected");
	});
});

