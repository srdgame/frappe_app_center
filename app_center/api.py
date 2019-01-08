# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import re
import requests
from frappe import throw, msgprint, _
from werkzeug.utils import secure_filename


app_props = ["name", "app_name", "owner", "category", "protocol", "star", "icon_image",
				"license_type", "device_supplier", "device_serial", "creation",
				"has_conf_template", "conf_template", "pre_configuration"]


@frappe.whitelist(allow_guest=True)
def list_apps(filters=None, fields=app_props, order_by="modified desc"):
	if filters:
		filters.update({"owner": ["!=", 'Administrator']})
	else:
		filters = {
			"owner": ["!=", 'Administrator'],
			"published": 1,
			"license_type": 'Open'
		}
	return frappe.get_all("IOT Application", fields=fields, filters=filters, order_by=order_by)


@frappe.whitelist()
def list_self_apps(fields=app_props, order_by="modified desc"):
	filters = {"owner": frappe.session.user}
	return frappe.get_all("IOT Application", fields=fields, filters=filters, order_by=order_by)


@frappe.whitelist(allow_guest=True)
def app_categories():
	return frappe.get_all("App Category", fields=["name", "description"])


@frappe.whitelist(allow_guest=True)
def app_suppliers():
	return frappe.get_all("App Device Supplier", fields=["name", "description"])


@frappe.whitelist(allow_guest=True)
def app_protocols():
	return frappe.get_all("App Device Protocol", fields=["name", "description"])


@frappe.whitelist(allow_guest=True)
def app_detail(app, fields=None):
	doc = frappe.get_doc('IOT Application', app)
	if fields is None:
		return doc
	data = {}
	for k in fields:
		data[k] = doc[k]
	return data


@frappe.whitelist(allow_guest=True)
def get_latest_version(app, beta=0):
	from app_center.doctype.iot_application_version.iot_application_version import get_latest_version as _get_latest_version
	return _get_latest_version(app, int(beta))


@frappe.whitelist(allow_guest=True)
def get_versions(app, beta=0, order_by="version desc"):
	filters = {
		"app": app
	}
	if int(beta) == 0:
		filters.update({
			"beta": 0
		})

	vlist = frappe.db.get_values("IOT Application Version", filters, "*", order_by=order_by)
	if not vlist:
		return None
	return vlist


@frappe.whitelist(allow_guest=True)
def check_update(app, beta=0):
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
	headers['Accept'] = 'application/json'


@frappe.whitelist(allow_guest=True)
def enable_beta(sn):
	iot_center = frappe.db.get_single_value("App Center Settings", "iot_center")
	if iot_center is None or iot_center == "":
		from iot.hdb_api import is_beta_enable
		return is_beta_enable(sn=sn)
	else:
		session = requests.session()
		# session.auth = (username, passwd)
		init_request_headers(session.headers)
		r = session.get(iot_center + "/api/method/iot.hdb_api.is_beta_enable", params={"sn":sn})
		if r.status_code != 200:
			throw(_("Cannot query beta information from IOT Center"))
		return r.json().get("message")


MATCH_APP_ID = re.compile(r'^APP(\d+)$')


def find_app_by_name(app):
	g = MATCH_APP_ID.match(app)
	if g:
		return frappe.get_doc("IOT Application", app)
	return frappe.get_doc("IOT Application", {"app_path": app})


@frappe.whitelist(allow_guest=True)
def user_access(app, user=None):
	user = user or frappe.session.user

	doc = find_app_by_name(app)
	if doc.license_type == 'Open':
		return True
	if doc.owner == user:
		return True

	# TODO: for application buy
	return False


@frappe.whitelist(allow_guest=True)
def company_access(app, company):
	user = frappe.session.user
	doc = find_app_by_name(app)
	if doc.license_type == 'Open':
		return True
	if doc.owner == user:
		return True

	# TODO: for application buy
	return False


@frappe.whitelist(allow_guest=True)
def user_access_device(sn):
	from iot.user_api import access_device
	try:
		if access_device(sn) is True:
			return True
		else:
			return False
	except Exception as ex:
		return False


@frappe.whitelist(allow_guest=True)
def ping():
	return _("pong")