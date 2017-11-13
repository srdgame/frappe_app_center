# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _


def get_comments():
	return frappe.db.get_all("IOT Application Comment",
								fields=["name", "comment", "owner", "modified", "reply_to"],
								limit=20,
								order_by="modified desc")


def get_reviews():
	return frappe.db.get_all("IOT Application Review",
								fields=["name", "star", "title", "content", "owner", "modified"],
								limit=20,
								order_by="modified desc")


def get_issues():
	return frappe.db.get_all("IOT Application Issue",
								fields=["name", "priority", "title", "content", "owner", "modified"],
								filters={"status": "Open"},
								limit=20,
								order_by="modified desc")


def get_context(context):
	app = frappe.form_dict.app
	if not app:
		raise frappe.DoesNotExistError(_("Application not specified"))

	tab = frappe.form_dict.tab or "description"

	doc = frappe.get_doc("IOT Application", app)

	context.no_cache = 0

	context.tab = tab
	context.doc = doc
	context.comments = get_comments()
	context.reviews = get_reviews()
	context.issues = get_issues()

	context.releases = frappe.db.get_all("IOT Application Version", fields="*", filters={"app": app}, limit=10, order_by="version desc")
	context.has_release = len(context.releases) > 0
