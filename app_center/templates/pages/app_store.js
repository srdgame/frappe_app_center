function jsonToQueryString(json) {
    return '?' +
        Object.keys(json).map(function(key) {
            return encodeURIComponent(key) + '=' +
                encodeURIComponent(json[key]);
        }).join('&');
};

$(document).ready(function() {
	$('.ui.app-refresh.button').click(function () {
		var query_data = {}
		var category = $('#category_filter .menu .item.selected').attr("value");
		if (category != null) {
			query_data["category"] = category;
		}
		var protocol = $('#protocol_filter .menu .item.selected').attr("value");
		if (protocol != null) {
			query_data["protocol"] = protocol;
		}
		var supplier = $('#supplier_filter .menu .item.selected').attr("value");
		if (supplier != null) {
			query_data["supplier"] = supplier;
		}

		window.location.href="/app_store"+jsonToQueryString(query_data);
	});
});

