# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from six.moves.urllib.parse import urlencode


def get_context(context):
	if frappe.session.user == 'Guest':
		frappe.local.flags.redirect_location = "/login?" + urlencode({"redirect-to": frappe.local.request.full_path})
		raise frappe.Redirect

	user_roles = frappe.get_roles(frappe.session.user)
	if 'App User' not in user_roles:
		raise frappe.PermissionError

	app = frappe.form_dict.app
	if not app:
		raise frappe.DoesNotExistError(_("Application not specified"))

	doc = frappe.get_doc("IOT Application", app)
	if frappe.session.user != 'Administrator' and doc.developer != frappe.session.user:
		raise frappe.PermissionError(_("You are not the developer of application {0}").format(doc.app_name))

	context.no_cache = 1

	context.categories = [d.name for d in frappe.get_all("App Category", ["name"], order_by="name")]
	context.protocols = [d.name for d in frappe.get_all("App Device Protocol", ["name"], order_by="name")]
	context.suppliers = [d.name for d in frappe.get_all("App Device Supplier", ["name"], order_by="name")]
	context.doc = doc
