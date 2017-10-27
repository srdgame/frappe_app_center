# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import os
import requests
from frappe import throw, msgprint, _
from werkzeug.utils import secure_filename


device_props = ["name", "app_name", "owner", "category", "protocol",
				"license_type", "device_supplier", "device_serial", "creation"]


@frappe.whitelist(allow_guest=True)
def list_apps(filters=None):
	return frappe.get_all("IOT Application", fields=device_props, filters=filters)


@frappe.whitelist(allow_guest=True)
def get_latest_version(app, beta):
	filters = {
		"app": app
	}
	if not beta:
		filters.update({
			"beta": 0
		})

	vlist = [d[0] for d in frappe.db.get_values("IOT Application Version", filters, "version")]
	if not vlist:
		return None
	return max(vlist)


@frappe.whitelist(allow_guest=True)
def check_update(app, beta=False):
	version = get_latest_version(app, beta)
	beta = frappe.get_value("IOT Application Version", {"app": app, "version": version}, "beta")
	return {
		"version": version,
		"beta": beta
	}


@frappe.whitelist(allow_guest=True)
def check_version(app, version):
	version = int(version)
	beta = frappe.get_value("IOT Application Version", {"app": app, "version": version}, "beta")
	if beta == 1:
		return "beta"
	if beta == 0:
		return "release"
	return "invalid"


@frappe.whitelist(allow_guest=True)
def get_forks(app):
	l = [d[0] for d in frappe.db.get_values("IOT Application", {"fork_from": app}, "name")]
	return l


def init_request_headers(headers):
	headers['Content-Type'] = 'application/json'
	headers['Accept'] = 'application/json'


@frappe.whitelist(allow_guest=True)
def enable_beta(sn):
	iot_center = frappe.db.get_single_value("App Center Settings", "iot_center")

	session = requests.session()
	# session.auth = (username, passwd)
	init_request_headers(session.headers)
	r = session.get(iot_center + "/api/method/iot.hdb_api.is_beta_enable", params={"sn":sn})
	if r.status_code != 200:
		throw(_("Cannot query beta information from IOT Center"))
	return r.json().get("message")