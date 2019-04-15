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
	user = frappe.session.user

	apps = frappe.get_list("IOT Application", "*", {"owner": user})
	context.apps = {d.name:d for d in apps}

	app_list = [d.name for d in apps]
	issues = frappe.get_list("IOT Application Issue", "*", {"app": ["in", app_list], "status": "Open"},  order_by="modified desc")

	context.issues = issues
	context.total_open = len(issues)

	count_closed_sql = "select count(*) from `tabIOT Application Issue` where owner='{0}' and status='Closed'".format(user)
	context.total_fixed = frappe.db.sql(count_closed_sql)[0][0]

	count_invalid_sql = "select count(*) from `tabIOT Application Issue` where owner='{0}' and status='Invalid'".format(user)
	context.total_invalid = frappe.db.sql(count_invalid_sql)[0][0]