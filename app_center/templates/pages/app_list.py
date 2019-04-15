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

	context.no_cache = 1

	category = frappe.form_dict.category

	context.categories = [d.name for d in frappe.db.get_all("App Category", ["name"], order_by="name")]

	filters = {"owner": frappe.session.user}
	if category:
		filters["category"] = category

	context.apps = frappe.db.get_all("IOT Application", "*", filters, order_by="modified desc")

	context.filters = filters