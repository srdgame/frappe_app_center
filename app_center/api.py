# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import base64
import json
import time
import os
from frappe import throw, msgprint, _
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(['csv', 'CSV', 'zip', 'ZIP', 'gz', 'GZ'])


def allowed_file(filename):
	# 用于判断文件后缀
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def decode_input(form_dict, key):
	val = form_dict.get(key)
	if val:
		return val.decode('utf-8')


def decode_input_checkbox(form_dict, key):
	val = form_dict.get(key)
	if val:
		return val.decode('utf-8') == 'on'
	return False


def app_remove(app, version):
	basedir = frappe.db.get_single_value('App Center Settings', 'release_folder')
	file_dir = os.path.join(basedir, app)

	ext = frappe.get_value("IOT Application", app, "app_ext")

	filename = str(version) + '.' + ext  # 修改了上传的文件名
	os.remove(os.path.join(file_dir, filename))


@frappe.whitelist()
def app_upload():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	version = int(decode_input(frappe.form_dict, 'version'))
	app = decode_input(frappe.form_dict, 'app')
	app_name = decode_input(frappe.form_dict, 'app_name')
	owner = decode_input(frappe.form_dict, 'owner') or frappe.session.user
	beta = decode_input_checkbox(frappe.form_dict, 'beta')

	if not version:
		throw(_("Application version not found!"))

	if not app or not app_name:
		throw(_("Application name not found!"))

	if not frappe.request.files:
		throw(_("Application file not found!"))

	f = frappe.request.files['app_file']  # 从表单的file字段获取文件，app_file为该表单的name值
	fname = secure_filename(f.filename)

	if f and allowed_file(fname):  # 判断是否是允许上传的文件类型
		basedir = frappe.db.get_single_value('App Center Settings', 'release_folder')
		# file_dir = os.path.join(basedir, owner)
		# if not os.path.exists(file_dir):
		# 	os.makedirs(file_dir)
		file_dir = os.path.join(basedir, app)
		if not os.path.exists(file_dir):
			os.makedirs(file_dir)

		ext = fname.rsplit('.', 1)[1].lower()  # 获取文件后缀
		if ext != frappe.get_value("IOT Application", app, "app_ext"):
			throw(_("Appication file extension name incorrect!"))

		new_filename = str(version) + '.' + ext  # 修改了上传的文件名
		# if beta:
		# 	new_filename = "beta_" + new_filename
		# print(new_filename)
		f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录

		data = {
			"doctype": "IOT Application Version",
			"app": app,
			"app_name": app_name,
			"version": version,
			"owner": owner,
			"beta": 0,
		}
		if beta:
			data.update({"beta": 1})

		try:
			doc = frappe.get_doc(data).insert()
			doc.save()
		except Exception as ex:
			os.remove(os.path.join(file_dir, new_filename))
			throw(_("Application version creation failed!"))

		return _("Application upload success")
	else:
		throw(_("Application upload failed!"))


device_props = ["name", "app_name", "owner", "category", "protocol",
				"license_type", "device_supplier", "device_serial", "creation"]


@frappe.whitelist(allow_guest=True)
def list_apps(filters=None):
	return frappe.get_all("IOT Application", fields=device_props, filters=filters)


@frappe.whitelist(allow_guest=True)
def get_latest_version(app, beta):
	l = [d[0] for d in frappe.db.get_values("IOT Application Version", {"app": app, "beta": beta}, "version")]
	if not l:
		return None
	return max(l)


@frappe.whitelist(allow_guest=True)
def check_update(app, beta=False):
	if not beta:
		return get_latest_version(app, 0)
	else:
		return get_latest_version(app, 1)


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


@frappe.whitelist(allow_guest=True)
def enable_beta(sn):
	user = frappe.db.get_single_value("IOT HDB Settings", "on_behalf")
	# form dict keeping
	form_dict = frappe.local.form_dict
	frappe.set_user(user)
	frappe.local.form_dict = form_dict

	return frappe.get_value("IOT Device", sn, "use_beta")
