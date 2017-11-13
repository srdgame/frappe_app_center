# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import redis
import json
from frappe import throw, _
from iot.iot.doctype.iot_hdb_settings.iot_hdb_settings import IOTHDBSettings


def list_install_apps(device):
	server = IOTHDBSettings.get_redis_server()
	print(server)
	if not server:
		throw(_("Redis Server is empty in IOT HDB Settings"))
	client = redis.Redis.from_url(server + "/6")
	return json.loads(client.get(device) or "")


def get_context(context):
	if frappe.session.user == 'Guest':
		frappe.local.flags.redirect_location = "/login"
		raise frappe.Redirect

	context.no_cache = 1

	issue = frappe.form_dict.issue
	if not issue:
		raise frappe.PermissionError(_("Application issue is missing!"))

	doc = frappe.get_doc('IOT Application Issue', issue)

	context.doc = doc
