# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import os
import json
from frappe import throw, msgprint, _
from frappe.utils import get_files_path
from werkzeug.utils import secure_filename



ALLOWED_EXTENSIONS = set(['csv', 'CSV', 'zip', 'ZIP', 'gz', 'GZ'])


def allowed_file(filename):
	# 用于判断文件后缀
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@frappe.whitelist()
def remove(app, version):
	basedir = get_files_path('app_center_files')
	file_dir = os.path.join(basedir, app)

	ext = frappe.get_value("IOT Application", app, "app_ext")

	filename = str(version) + '.' + ext  # 修改了上传的文件名
	os.remove(os.path.join(file_dir, filename))


@frappe.whitelist()
def upload():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	version = int(frappe.form_dict.version)
	app = frappe.form_dict.app
	app_name = frappe.form_dict.app_name
	owner = frappe.form_dict.owner or frappe.session.user
	comment = frappe.form_dict.comment or "Unknown comment"

	if not version:
		throw(_("Application version not found!"))

	if not app or not app_name:
		throw(_("Application name not found!"))

	if not frappe.request.files:
		throw(_("Application file not found!"))

	if frappe.get_value("IOT Application Version", {"app": app, "version":version}, "name"):
		throw(_("Application version duplicated!"))

	f = frappe.request.files['app_file']  # 从表单的file字段获取文件，app_file为该表单的name值
	fname = secure_filename(f.filename)

	if f and allowed_file(fname):  # 判断是否是允许上传的文件类型
		basedir = get_files_path('app_center_files')
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
		f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录

		data = {
			"doctype": "IOT Application Version",
			"app": app,
			"app_name": app_name,
			"version": version,
			"owner": owner,
			"beta": 1,
			"comment": comment,
		}

		try:
			doc = frappe.get_doc(data).insert()
			doc.save()
		except Exception as ex:
			os.remove(os.path.join(file_dir, new_filename))
			throw(_("Application version creation failed!"))

		return _("Application upload success")
	else:
		throw(_("Application upload failed!"))


def save_app_icon(app, f):
	fname = secure_filename(f.filename)
	ext = fname.rsplit('.', 1)[1].lower()  # 获取文件后缀
	if ext not in ['png', 'PNG']:
		throw(_("Application icon must be png file!"))

	basedir = get_files_path('app_center_files')
	file_dir = os.path.join(basedir, app)
	if not os.path.exists(file_dir):
		os.makedirs(file_dir)
	f.save(os.path.join(file_dir, "icon.png"))  # 保存文件到upload目录


@frappe.whitelist()
def new():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	app_name = frappe.form_dict.app_name
	license_type = frappe.form_dict.license_type
	category = frappe.form_dict.category
	protocol = frappe.form_dict.protocol
	device_supplier = frappe.form_dict.device_supplier
	device_serial = frappe.form_dict.device_serial
	description = frappe.form_dict.description
	owner = frappe.session.user
	doc = frappe.get_doc({
		"doctype": "IOT Application",
		"app_name": app_name,
		"license_type": license_type,
		"category": category,
		"protocol": protocol,
		"device_supplier": device_supplier,
		"device_serial": device_serial,
		"owner": owner,
		"description": description,
	}).insert()

	f = frappe.request.files['icon_file']  # 从表单的file字段获取文件，app_file为该表单的name值
	if f:
		save_app_icon(doc.name, f)

	return doc


@frappe.whitelist()
def modify():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	app_name = frappe.form_dict.app_name
	category = frappe.form_dict.category
	protocol = frappe.form_dict.protocol
	device_supplier = frappe.form_dict.device_supplier
	device_serial = frappe.form_dict.device_serial
	description = frappe.form_dict.description

	app = frappe.form_dict.app
	doc = frappe.get_doc("IOT Application", app)
	doc.set("app_name", app_name)
	doc.set("category", category)
	doc.set("protocol", protocol)
	doc.set("device_supplier", device_supplier)
	doc.set("device_serial", device_serial)
	doc.set("description", description)
	doc.save()

	f = frappe.request.files['icon_file']  # 从表单的file字段获取文件，app_file为该表单的name值
	if f:
		save_app_icon(doc.name, f)

	return doc


@frappe.whitelist()
def fork():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	version = int(frappe.form_dict.version)
	app = frappe.form_dict.app
	if not frappe.get_value('IOT Application Version', {"app": app, "version": version}, "name"):
		throw(_("Application version does not exists!"))

	doc = frappe.get_doc("IOT Application", app)
	owner = frappe.session.user

	new_doc = frappe.get_doc({
		"doctype": "IOT Application",
		"app_name": doc.app_name + "." + version,
		"license_type": doc.license_type,
		"category": doc.category,
		"protocol": doc.protocol,
		"device_supplier": doc.device_supplier,
		"device_serial": doc.device_serial,
		"owner": owner,
		"description": doc.description,
	}).insert()
	return new_doc


def fire_raw_content(content, status=200, content_type='text/html'):
	"""
	I am hack!!!
	:param content:
	:param content_type:
	:return:
	"""
	frappe.response['http_status_code'] = status
	frappe.response['filename'] = ''
	frappe.response['filecontent'] = content
	frappe.response['content_type'] = content_type
	frappe.response['type'] = 'download'


def get_app_file_path(app, fn):
	basedir = get_files_path('app_center_files')
	return os.path.join(basedir, app, fn)


def list_nodes(app, sub_folder):
	nodes = []
	app_folder = get_app_file_path(app, sub_folder)
	print(app_folder)
	for root, dirs, files in os.walk(app_folder, topdown=False):
		for name in dirs:
			nodes.append({
				"id": os.path.join(sub_folder, name),
				"text": name,
				"children": True,
				"icon": "folder"
			})
		for name in files:
			ext = name.rsplit('.', 1)[1].lower()  # 获取文件后缀
			nodes.append({
				"id": os.path.join(sub_folder, name),
				"text": name,
				"children": False,
				"type": "file",
				"icon": "file file-" + ext,
			})
	return nodes


def read_text_file_content(fpath):
	file_object = open(fpath)
	try:
		all_the_text = file_object.read()
		return all_the_text
	finally:
		file_object.close()


def read_binrary_file_url(app, fn):
	basedir = '/files/app_center_files'
	return os.path.join(basedir, app, fn)


read_content_map = {
	'text': read_text_file_content,
	'txt': read_text_file_content,
	'md': read_text_file_content,
	'htaccess': read_text_file_content,
	'log': read_text_file_content,
	'sql': read_text_file_content,
	'php': read_text_file_content,
	'js': read_text_file_content,
	'json': read_text_file_content,
	'css': read_text_file_content,
	'html': read_text_file_content,
}


def get_content(app, fn):
	fpath = get_app_file_path(app, fn)
	if os.path.isfile(fpath):
		ext = fn.rsplit('.', 1)[1].lower()  # 获取文件后缀
		read_fn = read_content_map.get(ext)
		content = read_binrary_file_url(app, fn)
		if read_fn:
			content = read_fn(fpath)
		return {
			'type': ext,
			'content': content
		}


@frappe.whitelist()
def editor():
	user = frappe.session.user
	app = frappe.form_dict.app
	app_name = frappe.get_value("IOT Application", app, "app_name")
	operation = frappe.form_dict.operation
	id = frappe.form_dict.id

	if operation == 'get_node':
		nodes = []
		if id == '#':
			nodes.append({
				"id": "/",
				'text': app_name,
				"icon": "folder",
				"state": {
					"opened": True,
					"disabled": True
				},
				'children': list_nodes(app, "")
			})
		else:
			nodes = list_nodes( app, id )

		fire_raw_content( json.dumps(nodes), 200, 'application/json' )

	if operation == 'get_content':
		content = get_content(app, id)
		fire_raw_content( json.dumps(content), 200, 'application/json' )