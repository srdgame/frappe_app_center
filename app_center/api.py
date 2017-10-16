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


ALLOWED_EXTENSIONS = set(['csv', 'CSV', 'zip', 'ZIP'])


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


@frappe.whitelist()
def app_upload():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	version = int(decode_input(frappe.form_dict, 'version'))
	app = decode_input(frappe.form_dict, 'app')
	app_name = decode_input(frappe.form_dict, 'app_name')
	owner = decode_input(frappe.form_dict, 'owner')
	beta = decode_input_checkbox(frappe.form_dict, 'beta')
	print(app, app_name, owner, beta, version)

	if not frappe.request.files:
		throw(_("Attachment file not found!"))

	f = frappe.request.files['app_file']  # 从表单的file字段获取文件，app_file为该表单的name值
	fname = secure_filename(f.filename)

	if f and allowed_file(fname):  # 判断是否是允许上传的文件类型
		ext = fname.rsplit('.', 1)[1]  # 获取文件后缀

		new_filename = str(version) + '.' + ext  # 修改了上传的文件名
		if beta:
			new_filename = "beta_" + new_filename
		print(new_filename)
		f.save(os.path.join("/tmp/", new_filename))  # 保存文件到upload目录

		return _("Upload Success")
	else:
		throw(_("Upload Failed!"))