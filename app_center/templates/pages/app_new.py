# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _


def get_context(context):
	user_roles = frappe.get_roles(frappe.session.user)
	if 'App User' not in user_roles or frappe.session.user == 'Guest':
		raise frappe.PermissionError

	context.no_cache = 0

	context.categories = [d.name for d in frappe.get_all("App Category", ["name"], order_by="name")]
	context.protocols = [d.name for d in frappe.get_all("App Device Protocol", ["name"], order_by="name")]
	context.suppliers = [d.name for d in frappe.get_all("App Device Supplier", ["name"], order_by="name")]
