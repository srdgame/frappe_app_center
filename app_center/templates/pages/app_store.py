# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _


def get_context(context):
	context.show_sidebar = True

	context.categories = [d.name for d in frappe.get_all("App Category", ["name"])]
	context.protocols = [d.name for d in frappe.get_all("App Device Protocol", ["name"])]
	context.suppliers = [d.name for d in frappe.get_all("App Device Supplier", ["name"])]
	context.apps = frappe.db.get_all("IOT Application", "*")
