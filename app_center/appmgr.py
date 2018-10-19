# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import os
import shutil
from frappe import throw, msgprint, _
from frappe.utils import get_files_path
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(['csv', 'CSV', 'zip', 'ZIP', 'gz', 'GZ', 'tgz', 'TGZ'])


def allowed_file(filename):
	# 用于判断文件后缀
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_app_release_path(app):
	basedir = get_files_path('app_center_files')
	file_dir = os.path.join(basedir, app)
	if not os.path.exists(file_dir):
		os.makedirs(file_dir)

	return file_dir


def get_app_release_filepath(app, version):
	file_dir = get_app_release_path(app)
	ext = frappe.get_value("IOT Application", app, "app_ext")
	filename = str(version) + '.' + ext
	return os.path.join(file_dir, filename)


def valid_app_owner(app):
	if frappe.session.user == 'Administrator':
		return
	if not "App Manager" in frappe.get_roles():
		return
	if frappe.get_value('IOT Application', app, 'owner') != frappe.session.user:
		raise frappe.PermissionError(_("You are not owner of application {0}").format(app))


@frappe.whitelist()
def remove_version_file(app, version):
	valid_app_owner(app)
	os.remove(get_app_release_filepath(app, version))
	os.remove(get_app_release_filepath(app, version) + ".md5")


def copy_to_latest(app, version, beta=1):
	valid_app_owner(app)

	from_file = get_app_release_filepath(app, version)
	to_file = get_app_release_filepath(app, "latest.beta" if beta == 1 else "latest")

	shutil.copy(from_file, to_file)
	shutil.copy(from_file + ".md5", to_file + ".md5")


@frappe.whitelist()
def remove_app_folder(app):
	valid_app_owner(app)
	shutil.rmtree(get_app_release_path(app))


@frappe.whitelist()
def upload():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	version = int(frappe.form_dict.version)
	app = frappe.form_dict.app
	comment = frappe.form_dict.comment or "Unknown comment"

	valid_app_owner(app)

	if not version:
		throw(_("Application version not found!"))

	if not app:
		throw(_("Application name not found!"))

	if not frappe.request.files:
		throw(_("Application file not found!"))

	if frappe.get_value("IOT Application Version", {"app": app, "version":version}, "name"):
		throw(_("Application version duplicated!"))

	f = frappe.request.files['app_file']  # 从表单的file字段获取文件，app_file为该表单的name值
	fname = secure_filename(repr(f.filename))

	if f and allowed_file(fname):  # 判断是否是允许上传的文件类型
		file_dir = get_app_release_path(app)

		ext = fname.rsplit('.', 1)[1].lower()  # 获取文件后缀
		ext_wanted = frappe.get_value("IOT Application", app, "app_ext")
		if ext != ext_wanted and ext_wanted != "tar.gz":
			throw(_("Appication file extension name incorrect!"))

		new_filename = os.path.join(file_dir, str(version) + '.' + ext_wanted)  # 修改了上传的文件名
		f.save(new_filename)  # 保存文件到upload目录

		data = {
			"doctype": "IOT Application Version",
			"app": app,
			"version": version,
			"beta": 1,
			"comment": comment,
		}

		try:
			doc = frappe.get_doc(data).insert()
			os.system("md5sum " + new_filename + " > " + new_filename + ".md5")
			shutil.copy(new_filename, os.path.join(file_dir, 'latest.beta.' + ext_wanted))
			shutil.copy(new_filename + ".md5", os.path.join(file_dir, 'latest.beta.' + ext_wanted + ".md5"))
		except Exception as ex:
			os.remove(new_filename)
			throw(_("Application version creation failed!"))

		return _("Application upload success")
	else:
		throw(_("Application upload failed!"))


def save_app_icon(app, f):
	fname = secure_filename(repr(f.filename))
	ext = fname.rsplit('.', 1)[1].lower()  # 获取文件后缀
	if ext not in ['png', 'PNG']:
		throw(_("Application icon must be png file!"))

	file_path = os.path.join(get_app_release_path(app), "icon.png")
	f.save(file_path)  # 保存文件到upload目录

	return "/files/app_center_files/" + app + "/icon.png"


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

	f = frappe.request.files.get('icon_file')  # 从表单的file字段获取文件，app_file为该表单的name值
	if f:
		file_path = save_app_icon(doc.name, f)
		doc.set("icon_image", file_path)
		doc.save()

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
	valid_app_owner(app)
	doc.set("app_name", app_name)
	doc.set("category", category)
	doc.set("protocol", protocol)
	doc.set("device_supplier", device_supplier)
	doc.set("device_serial", device_serial)
	doc.set("description", description)

	f = frappe.request.files.get('icon_file')  # 从表单的file字段获取文件，app_file为该表单的name值
	if f:
		file_path = save_app_icon(doc.name, f)
		doc.set("icon_image", file_path)

	doc.save()

	return doc


def copy_app_release_file(from_app, to_app, version):
	from_file = get_app_release_filepath(from_app, version)
	to_file = get_app_release_filepath(to_app, version)
	shutil.copy(from_file, to_file)
	shutil.copy(from_file + ".md5", to_file + ".md5")


def copy_app_icon_file(from_app, to_app):
	from_icon = os.path.join(get_app_release_path(from_app), "icon.png")
	if not os.path.exists(from_icon):
		return
	to_icon = os.path.join(get_app_release_path(to_app), "icon.png")
	shutil.copy(from_icon, to_icon)


def copy_forked_app_files(from_app, to_app, version):
	frappe.get_doc({
		"doctype": "IOT Application Version",
		"app": to_app,
		"version": version,
		"comment": frappe.get_value('IOT Application Version', {"app": from_app, "version": version}, "comment"),
		"beta": frappe.get_value('IOT Application Version', {"app": from_app, "version": version}, "beta")
	}).insert()
	copy_app_release_file(from_app, to_app, version)
	copy_app_icon_file(from_app, to_app)


@frappe.whitelist()
def fork():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	version = int(frappe.form_dict.version)
	app = frappe.form_dict.app
	if not frappe.get_value('IOT Application Version', {"app": app, "version": version}, "name"):
		throw(_("Application version {0} does not exists!").format(version))

	doc = frappe.get_doc("IOT Application", app)
	forked_doc = doc.fork(frappe.session.user, version)

	copy_forked_app_files(app, forked_doc.name, version)

	return forked_doc.name


@frappe.whitelist()
def get_fork(app, version, owner=None):
	from app_center.doctype.iot_application_version.iot_application_version import get_latest_version
	owner = owner or frappe.session.user
	doc = frappe.get_doc("IOT Application", app)
	app = doc.get_fork(owner, version)
	lver = get_latest_version(app, 1)
	return app, lver


@frappe.whitelist()
def add_review():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))
	app = frappe.form_dict.app
	star = frappe.form_dict.star
	title = frappe.form_dict.title
	content = frappe.form_dict.content.replace('\n', '<br>')
	doc = frappe.get_doc({
		"doctype": "IOT Application Review",
		"app": app,
		"star": star,
		"title": title,
		"content": content,
	}).insert()

	return _("Review added!")


@frappe.whitelist()
def remove_review():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	name = frappe.form_dict.name
	frappe.delete_doc("IOT Application Review", name)

	return _("Review deleted!")


@frappe.whitelist()
def add_review_comment():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	review = frappe.form_dict.review
	comment = frappe.form_dict.comment.replace('\n', '<br>')
	doc = frappe.get_doc("IOT Application Review", review)
	doc.append("comments", {"comment": comment, "owner": frappe.session.user})
	doc.save(ignore_permissions=True)

	return _("Review comment added!")


@frappe.whitelist()
def remove_review_comment():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	parent = frappe.form_dict.parent
	name = frappe.form_dict.name
	doc = frappe.get_doc("IOT Application Review", parent)
	for comm in doc.comments:
		if comm.name == name and comm.owner == frappe.session.user:
			doc.remove(comm)
			doc.save(ignore_permissions=True)
			return _("Review comment removed!")

	return _("Review comment not found!")


@frappe.whitelist()
def add_comment():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	app = frappe.form_dict.app
	comment = frappe.form_dict.comment.replace('\n', '<br>')
	reply_to = frappe.form_dict.reply_to
	doc = frappe.get_doc({
		"doctype": "IOT Application Comment",
		"app": app,
		"comment": comment,
		"reply_to": reply_to
	}).insert()

	return _("Comment added!")


@frappe.whitelist()
def remove_comment():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	name = frappe.form_dict.name
	frappe.delete_doc("IOT Application Comment", name)

	return _("Comment removed!")


@frappe.whitelist()
def add_issue():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	app = frappe.form_dict.app
	title = frappe.form_dict.title
	priority = frappe.form_dict.priority
	content = frappe.form_dict.content.replace('\n', '<br>')
	doc = frappe.get_doc({
		"doctype": "IOT Application Issue",
		"app": app,
		"title": title,
		"priority": priority,
		"content": content,
	}).insert()

	return _("Issue added!")


@frappe.whitelist()
def remove_issue():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	name = frappe.form_dict.name
	frappe.delete_doc("IOT Application Issue", name)

	return _("Issue removed!")


@frappe.whitelist()
def add_issue_comment():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	issue = frappe.form_dict.issue
	comment = frappe.form_dict.comment.replace('\n', '<br>')
	doc = frappe.get_doc("IOT Application Issue", issue)
	doc.append("comments", {"comment": comment, "owner": frappe.session.user})
	doc.save(ignore_permissions=True)

	return _("Issue comment added!")


@frappe.whitelist()
def remove_issue_comment():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	parent = frappe.form_dict.parent
	name = frappe.form_dict.name
	doc = frappe.get_doc("IOT Application Issue", parent)
	for comm in doc.comments:
		if comm.name == name and comm.owner == frappe.session.user:
			doc.remove(comm)
			doc.save(ignore_permissions=True)
			return _("Issue comment removed!")

	return _("Issue comment not found!")


@frappe.whitelist()
def fix_issue():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	issue = frappe.form_dict.issue
	action = frappe.form_dict.action
	comment = "Action: " + action + "\r\n" + frappe.form_dict.comment

	doc = frappe.get_doc("IOT Application Issue", issue)
	doc.status = action
	doc.append("comments", {"comment": comment})
	doc.save()

	return _("Issue fixed!")


@frappe.whitelist()
def ping():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))

	return _("pong")