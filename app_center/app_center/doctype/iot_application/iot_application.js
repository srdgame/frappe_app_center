// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('IOT Application', {
	refresh: function(frm) {
		frm.add_custom_button(__("Update Stars"), function() {
			frm.events.update_stars(frm);
		}).removeClass("btn-default").addClass("btn-warning");
	},
	update_stars: function(frm) {
		return frappe.call({
			doc: frm.doc,
			method: "update_stars",
			freeze: true,
			callback: function(r) {
				if(!r.exc) frm.refresh_fields();
			}
		})
	},
});
