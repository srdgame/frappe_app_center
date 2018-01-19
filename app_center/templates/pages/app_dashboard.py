# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _


def get_most_stars():
	filters = {"owner": ["!=", 'Administrator']}
	return frappe.db.get_all("IOT Application", filters=filters, fields="*", limit=5, order_by="star desc")


def get_recently_updated():
	filters = {"owner": ["!=", 'Administrator']}
	return frappe.db.get_all("IOT Application", filters=filters, fields="*", limit=5, order_by="modified desc")

def get_latest_releases():
	filters = {"owner": ["!=", 'Administrator']}
	return frappe.db.get_all("IOT Application Version", filters=filters, fields="*", limit=5, order_by="creation desc")


def get_context(context):
	context.no_cache = 1

	category = frappe.form_dict.category

	context.categories = [d.name for d in frappe.db.get_all("App Category", ["name"], order_by="name")]

	filters = {"owner": frappe.session.user}
	if category:
		filters["category"] = category

	context.apps = frappe.db.get_all("IOT Application", "*", filters, order_by="star desc", limit=3)

	context.filters = filters
	context.most_stars = get_most_stars()
	context.recently_updated = get_recently_updated()
	context.releases = get_latest_releases()


	count_apps = "select count(*) from `tabIOT Application` where owner<>'Administrator'" # and published=1
	context.application_count = frappe.db.sql(count_apps)[0][0]

	count_developers = "select count(*) from `tabApp Developer` where user<>'Administrator'"
	context.developer_count = frappe.db.sql(count_developers)[0][0]

	count_suppliers = "select count(*) from `tabApp Device Supplier`"
	context.supplier_count = frappe.db.sql(count_suppliers)[0][0]