# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _


def get_context(context):

	category = frappe.form_dict.category
	protocol = frappe.form_dict.protocol
	device_supplier = frappe.form_dict.device_supplier

	context.categories = [d.name for d in frappe.get_all("App Category", ["name"], order_by="name")]
	context.protocols = [d.name for d in frappe.get_all("App Device Protocol", ["name"], order_by="name")]
	context.suppliers = [d.name for d in frappe.get_all("App Device Supplier", ["name"], order_by="name")]

	filters = {"owner": ["!=", 'Administrator']}
	if category:
		filters["category"] = category
	if protocol:
		filters["protocol"] = protocol
	if device_supplier:
		filters["device_supplier"] = device_supplier

	context.apps = frappe.db.get_all("IOT Application", "*", filters, order_by="modified desc")
	context.filters = filters

