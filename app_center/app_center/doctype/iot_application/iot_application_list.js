frappe.listview_settings['IOT Application'] = {
	onload: function(listview) {

		listview.page.add_menu_item(__("Update Package Path"), function() {
			var method = "app_center.app_center.doctype.iot_application.iot_application.update_apps_path";
			listview.call_for_selected_items(method, {"status": ""});
		});

		/*
		listview.page.add_menu_item(__("Update Starts"), function() {
			var method = "app_center.app_center.doctype.iot_application.iot_application.update_apps_stars";
			listview.call_for_selected_items(method, {"status": ""});
		});
		*/

	}
};
