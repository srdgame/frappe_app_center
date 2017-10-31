# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _


def get_most_stars():
	return frappe.get_list("IOT Application", fields="*", limit=5, order_by="app_name")


def get_recently_updated():
	return frappe.get_list("IOT Application", fields="*", limit=5, order_by="modified desc")


def get_context(context):
	if frappe.session.user == 'Guest':
		frappe.local.flags.redirect_location = "/login"
		raise frappe.Redirect

	context.no_cache = 1

	category = frappe.form_dict.category

	context.categories = [d.name for d in frappe.db.get_all("App Category", ["name"], order_by="name")]

	filters = {"owner": frappe.session.user}
	if category:
		filters["category"] = category

	context.apps = frappe.db.get_all("IOT Application", "*", filters, order_by="modified desc")

	context.filters = filters
	context.most_stars = get_most_stars()
	context.recently_updated = get_recently_updated()