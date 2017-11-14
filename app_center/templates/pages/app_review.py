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

	name = frappe.form_dict.name
	if not name:
		raise frappe.PermissionError(_("Application review name is missing!"))

	doc = frappe.get_doc('IOT Application Review', name)

	context.doc = frappe.get_doc('IOT Application', doc.app)
	context.review = doc
	context.has_release = frappe.get_value("IOT Application Version", {"app": doc.app})
