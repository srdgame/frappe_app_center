# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from urllib import urlencode


def get_context(context):
	if frappe.session.user == 'Guest':
		frappe.local.flags.redirect_location = "/login?" + urlencode({"redirect-to": frappe.local.request.full_path})
		raise frappe.Redirect

	context.no_cache = 1

	apps = frappe.get_list("IOT Application", "*", {"owner": frappe.session.user})
	context.apps = {d.name:d for d in apps}

	app_list = [d.name for d in apps]
	issues = frappe.get_list("IOT Application Issue", "*", {"app": ["in", app_list], "Status": "Open"},  order_by="modified desc")

	context.issues = issues