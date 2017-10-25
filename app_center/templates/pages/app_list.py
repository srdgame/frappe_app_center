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

	context.no_cache = 1
	context.show_sidebar = True

	context.categories = [d.name for d in frappe.db.get_all("App Category", ["name"], order_by="name")]
	if frappe.session.user != 'Administrator':
		context.apps = frappe.db.get_all("IOT Application", "*", {"owner": frappe.session.user}, order_by="modified desc")
	else:
		context.apps = frappe.db.get_all("IOT Application", "*", order_by="modified desc")

