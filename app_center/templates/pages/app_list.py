# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _


def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True

	context.categories = [d.name for d in frappe.db.get_all("App Category", ["name"])]
	context.doc = {
		"apps": {}
	}
