function jsonToQueryString(json) {
    return '?' +
        Object.keys(json).map(function(key) {
            return encodeURIComponent(key) + '=' +
                encodeURIComponent(json[key]);
        }).join('&');
};

$(document).ready(function() {
	$('.ui.items .item .content .meta .ui.star.rating')
	  .rating('disable')
	;
	$('.ui.items .item .content .extra .upload').click(function () {
		var app = $(this).data("name");
		window.location.href="/app_upload?app="+app;
	});
	$('.ui.items .item .content .extra .modify').click(function () {
		var app = $(this).data("name");
		window.location.href="/app_modify?app="+app;
	});
	$('.ui.items .item .content .extra .comment').click(function() {
		var app = $(this).data("name");
		window.location.href="/app_detail?app="+app+"&tab=comments";
	});
	$('.ui.items .item .content .extra .star').click(function() {
		var app = $(this).data("name");
		window.location.href="/app_detail?app="+app+"&tab=reviews";
	});

	$('.ui.items .item .description .labels .label.category').click(function() {
		var cate = $(this).data('value');
		var cate_text = $(this).text();
		$('#category_filter').find('.text').html('<i class="ui teal empty circular label"></i> ' + cate_text);
		$('#category_filter .menu .item.selected').removeClass("active selected");
		$('#category_filter .menu [data-value="' + cate + '"]').addClass("active selected");
	});

	$('.ui.items .item .description .labels .label.protocol').click(function() {
		var proto = $(this).data('value');
		var proto_text = $(this).text();
		$('#protocol_filter').find('.text').html('<i class="ui blue empty circular label"></i> ' + proto_text);
		$('#protocol_filter .menu .item.selected').removeClass("active selected");
		$('#protocol_filter .menu [data-value="' + proto + '"]').addClass("active selected");
	});

	$('.ui.items .item .description .labels .label.supplier').click(function() {
		var supplier = $(this).data('value');
		var supplier_text = $(this).text();
		$('#supplier_filter').find('.text').html('<i class="ui olive empty circular label"></i> ' + supplier_text);
		$('#supplier_filter .menu .item.selected').removeClass("active selected");
		$('#supplier_filter .menu [data-value="' + supplier + '"]').addClass("active selected");
	});

	$('.ui.app-refresh.button').click(function () {
		var query_data = {};
		var category = $('#category_filter .menu .item.selected').data("value");
		if (category != null) {
			query_data["category"] = category;
		}
		var protocol = $('#protocol_filter .menu .item.selected').data("value");
		if (protocol != null) {
			query_data["protocol"] = protocol;
		}
		var supplier = $('#supplier_filter .menu .item.selected').data("value");
		if (supplier != null) {
			query_data["device_supplier"] = supplier;
		}

		window.location.href="/app_store"+jsonToQueryString(query_data);
	});
	$('.ui.app-clean.button').click(function () {
		//window.location.href="/app_store";
		$('#category_filter .text').text('{{_("Category Filter")}}');
		$('#category_filter .menu .item.selected').removeClass("active selected");
		$('#protocol_filter .text').text('{{_("Protocol Filter")}}');
		$('#protocol_filter .menu .item.selected').removeClass("active selected");
		$('#supplier_filter .text').text('{{_("Supplier Filter")}}');
		$('#supplier_filter .menu .item.selected').removeClass("active selected");
	});
});

