# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _


def get_context(context):
	app = frappe.form_dict.app
	if not app:
		raise frappe.DoesNotExistError(_("Application not specified"))

	doc = frappe.get_doc("IOT Application", app)

	context.no_cache = 0

	context.doc = doc
	context.comments = [
		{
			"author": "Administrator",
			"date": "2 days ago",
			"content": "The hours, minutes and seconds stand as visible reminders that your effort put them all there.",
		},
		{
			"author": "cch",
			"date": "3 days ago",
			"content": "Adfwccqqwe.",
		},
		{
			"author": "dirk",
			"date": "4 days ago",
			"content": "Reminders that.",
		}
	]
	context.releases = [
		{
			"version": 120,
			"date": "one week ago",
			"comment": "fixed ..xxxfaf ",
		},
		{
			"version": 100,
			"date": "one month ago",
			"comment": "First release",
		}
	]
