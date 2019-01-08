// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('IOT Application', {
	refresh: function(frm) {
		frm.add_custom_button(__("Update Stars"), function() {
			frm.events.update_stars(frm);
		}).removeClass("btn-default").addClass("btn-warning");

		frm.add_custom_button(__("Update Package Path"), function () {
			frm.events.update_app_path(frm);
		}).removeClass("btn-default").addClass("btn-warning");

		if (frappe.user.has_role(['Administrator','App Manager'])) {
			frm.add_custom_button(__("Clean Before Delete This"), function () {
				frm.events.clean_before_delete(frm);
			}).removeClass("btn-default").addClass("btn-warning");
		}
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
	update_app_path: function(frm) {
		return frappe.call({
			doc: frm.doc,
			method: "update_app_path",
			freeze: true,
			callback: function (r) {
				if (!r.exc) frm.refresh_fields();
			}
		})
	},
	clean_before_delete: function(frm) {
		return frappe.call({
			doc: frm.doc,
			method: "clean_before_delete",
			freeze: true,
			callback: function(r) {
				if(!r.exc) frm.refresh_fields();
			}
		})
	},
});
