# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _


def get_comments(app):
	comments = frappe.db.get_all("IOT Application Comment",
								filters={"app": app},
								fields=["name", "comment", "owner", "modified", "reply_to"],
								#limit=20,
								order_by="modified desc")
	comments.reverse()
	return comments


def get_reviews(app):
	return frappe.db.get_all("IOT Application Review",
								filters={"app": app},
								fields=["name", "star", "title", "content", "owner", "modified"],
								#limit=20,
								order_by="modified desc")


def get_issues(app):
	return frappe.db.get_all("IOT Application Issue",
								fields=["name", "priority", "title", "content", "owner", "modified"],
								filters={"status": "Open", "app": app},
								#limit=20,
								order_by="modified desc")


def get_releases(app):
	return frappe.db.get_all("IOT Application Version", fields="*", filters={"app": app}, limit=10, order_by="version desc")


def get_context(context):
	app = frappe.form_dict.app
	if not app:
		raise frappe.DoesNotExistError(_("Application not specified"))

	tab = frappe.form_dict.tab or "description"

	doc = frappe.get_doc("IOT Application", app)

	context.no_cache = 0

	context.tab = tab
	context.doc = doc
	context.comments = get_comments(app)
	context.reviews = get_reviews(app)
	context.issues = get_issues(app)

	context.releases =get_releases(app)
	context.has_release = len(context.releases) > 0
