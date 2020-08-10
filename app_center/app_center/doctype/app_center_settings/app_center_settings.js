// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('App Center Settings', {
	refresh: function(frm) {
		frm.add_custom_button(__("Synchronous IOT Center"), function() {
			frm.events.sync_app_center(frm);
		}).removeClass("btn-default").addClass("btn-primary");
	},
	sync_app_center: function(frm) {
		return frappe.call({
			doc: frm.doc,
			method: "sync_app_center",
			freeze: true,
			callback: function(r) {
				if(!r.exc) frm.reload_doc();
			}
		})
	}
});
