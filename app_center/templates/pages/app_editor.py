# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _


def get_context(context):
	if frappe.session.user == 'Guest':
		frappe.local.flags.redirect_location = "/login"
		raise frappe.Redirect

	app = frappe.form_dict.app
	if not app:
		raise frappe.DoesNotExistError(_("Application not specified"))

	device_link = frappe.form_dict.device
	app_inst = frappe.form_dict.app_inst
	version_want = int(frappe.form_dict.version)
	if device_link and (not app_inst or not version_want):
		raise frappe.ValidationError

	app_doc = frappe.get_doc("IOT Application", app)
	user_roles = frappe.get_roles(frappe.session.user)
	if 'App User' not in user_roles:
		raise frappe.PermissionError

	if frappe.session.user != 'Administrator' and app_doc.owner != frappe.session.user:
		raise frappe.PermissionError(_("You are not the owner of application {0}").format(app_doc.app_name))

	context.no_cache = 1

	context.doc = app_doc
	context.device_link = device_link
	context.app_inst = app_inst
	context.releases = frappe.db.get_all("IOT Application Version", fields="*", filters={"app": app}, limit=10, order_by="version desc")

	context.version_want = version_want
	if version_want is not None:
		if version_want < context.releases[0].version:
			context.show_version_warning = True