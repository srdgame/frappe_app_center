// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('IOT Application Version', {
	refresh: function(frm) {
		if (frm.doc.tested == 0 || !frm.doc.tested_date) {
			frm.add_custom_button(__("Tested"), function () {
				frm.events.set_tested(frm);
			}).removeClass("btn-default").addClass("btn-primary");
		}
		if (frm.doc.approved == 0 || !frm.doc.approved_date) {
			frm.add_custom_button(__("Approve"), function () {
				frm.events.set_approved(frm);
			}).removeClass("btn-default").addClass("btn-primary");
		}
	},
	set_tested: function(frm) {
		return frappe.call({
			doc: frm.doc,
			method: "set_tested",
			freeze: true,
			callback: function(r) {
				if(!r.exc) frm.refresh_fields();
			}
		})
	},
	set_approved: function(frm) {
		return frappe.call({
			doc: frm.doc,
			method: "set_approved",
			freeze: true,
			callback: function(r) {
				if(!r.exc) frm.refresh_fields();
			}
		})
	}
});
