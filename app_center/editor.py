# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import os
import json
import shutil
import zipfile
import codecs
from frappe import throw, msgprint, _
from frappe.utils import get_files_path
from app_center.appmgr import get_app_release_path, remove_version_file, valid_app_owner, copy_to_latest


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


def get_app_editor_file_path(app, fn=""):
	basedir = get_files_path('app_center_files')
	path = os.path.join(basedir, app, ".editor", fn)
	if len(path) < (len(basedir) + len(app) + len(fn)):
		print(basedir, app, fn, path)
		throw(_("EEEEEEEEEEEEEEEEEEEEEEE"))
	return path


def editor_list_nodes(app, sub_folder):
	nodes = []
	app_folder = get_app_editor_file_path(app, sub_folder)
	if hasattr(os, 'scandir'):
		for entry in os.scandir(app_folder):
			if not entry.name.startswith('.'):
				if entry.is_dir():
					nodes.append({
						"id": os.path.join(sub_folder, entry.name),
						"text": entry.name,
						"children": True,
						"type": "folder",
						"icon": "folder"
					})
				if entry.is_file():
					ext = os.path.splitext(entry.name)[1].lower()  # 获取文件后缀
					nodes.append({
						"id": os.path.join(sub_folder, entry.name),
						"text": entry.name,
						"children": False,
						"type": "file",
						"icon": "file file-" + ext,
					})
	else:
		for name in os.listdir(app_folder):
			if not name.startswith('.'):
				if os.path.isdir(os.path.join(app_folder, name)):
					nodes.append({
						"id": os.path.join(sub_folder, name),
						"text": name,
						"children": True,
						"type": "folder",
						"icon": "folder"
					})
				if os.path.isfile(os.path.join(app_folder, name)):
					ext = os.path.splitext(name)[1].lower()  # 获取文件后缀
					nodes.append({
						"id": os.path.join(sub_folder, name),
						"text": name,
						"children": False,
						"type": "file",
						"icon": "file" if ext == "" else "file file-" + ext[1:],
					})
	return nodes

def editor_get_node(app, node_id):
	if node_id == '#':
		code_name = frappe.get_value("IOT Application", app, "code_name") \
					or frappe.get_value("IOT Application", app, "app_name")

		app_folder = get_app_editor_file_path(app)
		if not os.path.exists(app_folder):
			os.makedirs(app_folder)
		return [{
			"id": "/",
			'text': code_name,
			"type": "folder",
			"icon": "folder",
			"state": {
				"opened": True,
				"disabled": True
			},
			'children': editor_list_nodes(app, "")
		}]
	else:
		return editor_list_nodes(app, node_id)


def editor_create_node(app, node_id, node_type, node_name):
	fn = os.path.join(node_id, node_name)
	fpath = get_app_editor_file_path(app, fn)
	if node_type == 'file':
		node = open(fpath, 'a')
		node.close()
		ext = os.path.splitext(node_name)[1].lower()  # 获取文件后缀
		if len(ext) > 0:
			return {"id": fn, "icon": "file file-"+ext[1:]}
	else:
		if not os.path.exists(fpath):
			os.makedirs(fpath)

	return {"id": fn}


def editor_rename_node(app, node_id, new_name):
	fpath = get_app_editor_file_path(app, node_id)
	try:
		if new_name != os.path.basename(fpath):
			new_node_id = os.path.join(os.path.dirname(node_id), new_name)
			new_path = get_app_editor_file_path(app, new_node_id)
			if not os.access(new_path, os.R_OK):
				os.rename(fpath, new_path)
				if os.path.isfile(new_path):
					ext = os.path.splitext(new_name)[1].lower()  # 获取文件后缀
					if len(ext) > 0:
						return {"id": new_node_id, "icon": "file file-"+ext[1:]}
				return {"id": new_node_id}
	except Exception:
		pass

	return {"id": node_id}


def editor_move_node(app, node_id, dst):
	if os.path.dirname(node_id) != dst:
		filename = os.path.basename(node_id)
		src = get_app_editor_file_path(app, node_id)
		dst_folder = get_app_editor_file_path(app, dst)
		if os.path.isdir(dst_folder):
			shutil.move(src, dst_folder)
			return {"id": os.path.join(dst, filename)}

	return {"id": node_id}


def editor_copy_node(app, node_id, dst):
	if os.path.dirname(node_id) != dst:
		src = get_app_editor_file_path(app, node_id)
		filename = os.path.basename(node_id)
		dst_folder = get_app_editor_file_path(app, dst)
		if os.path.isdir(src):
			shutil.copytree(src, os.path.join(dst_folder, filename))
		else:
			shutil.copy(src, dst_folder)
		return {"id": os.path.join(dst, filename)}


def editor_delete_node(app, node_id):
	fpath = get_app_editor_file_path(app, node_id)
	if os.path.isdir(fpath):
		shutil.rmtree(fpath)
	else:
		os.remove(fpath)
	return {"status": "OK"}


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
	'csv': read_text_file_content,
	'md': read_text_file_content,
	'htaccess': read_text_file_content,
	'log': read_text_file_content,
	'sql': read_text_file_content,
	'php': read_text_file_content,
	'js': read_text_file_content,
	'json': read_text_file_content,
	'css': read_text_file_content,
	'html': read_text_file_content,
	'lua': read_text_file_content,
	'py': read_text_file_content,
	'h': read_text_file_content,
	'c': read_text_file_content,
	'hpp': read_text_file_content,
	'cpp': read_text_file_content,
	'cxx': read_text_file_content,
}


def editor_get_content(app, node_id):
	fpath = get_app_editor_file_path(app, node_id)
	if os.path.isfile(fpath):
		ext = os.path.splitext(node_id)[1].lower()  # 获取文件后缀
		ext = "text" if ext == "" else ext[1:]
		read_fn = read_content_map.get(ext)
		content = read_binrary_file_url(app, node_id)
		if read_fn:
			content = read_fn(fpath)
		return {
			'type': ext,
			'content': content
		}

	if os.path.isdir(fpath):
		return {
			'type': 'folder',
		}


def editor_set_content(app, node_id, text):
	fpath = get_app_editor_file_path(app, node_id)
	if os.path.isfile(fpath):
		file_object = codecs.open(fpath, "w", "utf-8") #open(fpath, "w")
		file_object.write(text)
		file_object.close()
		return {"status": "OK"}


@frappe.whitelist()
def editor():
	app = frappe.form_dict.app
	operation = frappe.form_dict.operation
	node_id = frappe.form_dict.id if frappe.form_dict.id != "/" else ""
	valid_app_owner(app)

	content = None
	if operation == 'get_node':
		content = editor_get_node(app, node_id)

	if operation == 'create_node':
		type = frappe.form_dict.type
		text = frappe.form_dict.text
		content = editor_create_node(app, node_id, type, text)

	if operation == 'rename_node':
		text = frappe.form_dict.text
		content = editor_rename_node(app, node_id, text)

	if operation == 'move_node':
		dst = frappe.form_dict.parent if frappe.form_dict.parent != "/" else ""
		content = editor_move_node(app, node_id, dst)

	if operation == 'delete_node':
		if frappe.form_dict.id == "/":
			throw(_("Cannot remove root folder"))
		content = editor_delete_node(app, node_id)

	if operation == 'copy_node':
		dst = frappe.form_dict.parent if frappe.form_dict.parent != "/" else ""
		content = editor_copy_node(app, node_id, dst)

	if operation == 'get_content':
		content = editor_get_content(app, node_id)

	if operation == 'set_content':
		text = frappe.form_dict.text
		content = editor_set_content(app, node_id, text)

	if content is not None:
		fire_raw_content(json.dumps(content), 200, 'application/json; charset=utf-8')


def zip_application(app, version, editor=False):
	app_dir = get_app_release_path(app)
	app_file = os.path.join(app_dir, str(version) + '.zip')
	if editor:
		app_file = os.path.join(app_dir, str(version) + '.editor.zip')

	if os.access(app_file, os.R_OK):
		if editor:
			os.remove(app_file)
		else:
			throw(_("Application version already exits!"))

	editor_dir = get_app_editor_file_path(app)
	vf = open(os.path.join(editor_dir, "version"), 'w')
	vf.write(str(version))
	vf.write('\n')
	vf.write("WEB_EDITOR")
	vf.close()

	f = zipfile.ZipFile(app_file, 'w', zipfile.ZIP_DEFLATED)
	for root, dirs, files in os.walk(editor_dir):
		for filename in files:
			filename = os.path.join(root, filename)
			arcname = filename[len(editor_dir):]
			f.write(filename, arcname)
	f.close()
	return app_file


@frappe.whitelist()
def editor_release(app=None, version=None, comment=None):
	app = app or frappe.form_dict.app
	version = version or frappe.form_dict.version
	comment = comment or frappe.form_dict.comment
	if not app or not version or not comment:
		raise frappe.ValidationError

	valid_app_owner(app)

	data = {
		"doctype": "IOT Application Version",
		"app": app,
		"version": version,
		"beta": 1,
		"comment": comment,
	}

	app_file = zip_application(app, version)

	try:
		doc = frappe.get_doc(data).insert()
		os.system("md5sum " + app_file + " > " + app_file + ".md5")
	except Exception as ex:
		frappe.logger(__name__).error(repr(ex))
		remove_version_file(app, version)
		raise ex

	copy_to_latest(app, version)

	return _("Application upload success")


@frappe.whitelist()
def editor_init(app, version=None):
	from app_center.app_center.doctype.iot_application_version.iot_application_version import get_latest_version

	valid_app_owner(app)

	ver = editor_workspace_version(app)
	if ver:
		return ver

	version = version or get_latest_version(app, beta=1)

	if version is None:
		version = 0

	# Revert editor workspace to specified version
	if version > 0:
		editor_revert(app, version)
	else:
		editor_dir = get_app_editor_file_path(app)
		os.mkdir(editor_dir)

	# Make sure the workspace has correct version file
	if editor_workspace_version(app) is None:
		editor_dir = get_app_editor_file_path(app)
		vf = open(os.path.join(editor_dir, "version"), 'w')
		vf.write(str(version))
		vf.write('\n')
		vf.write("WEB_EDITOR")
		vf.close()

	return version


@frappe.whitelist()
def editor_revert(app=None, version=None, check_db=True):
	app = app or frappe.form_dict.app
	version = version or frappe.form_dict.version
	if not app or not version:
		raise frappe.ValidationError

	valid_app_owner(app)

	if check_db is True and not frappe.get_value("IOT Application Version", {"app": app, "version": version}, "name"):
		throw(_("Version {0} does not exits!").format(version))

	app_dir = get_app_release_path(app)
	app_file = os.path.join(app_dir, str(version) + '.zip')

	if not os.access(app_file, os.R_OK):
		throw(_("Version {0}  release file does not exits!").format(version))

	editor_dir = get_app_editor_file_path(app)
	shutil.rmtree(editor_dir, ignore_errors=True)
	os.mkdir(editor_dir)
	f = zipfile.ZipFile(app_file, 'r')
	f.extractall(editor_dir)
	f.close()

	return _("Workspace revert success!")


@frappe.whitelist()
def editor_workspace_version(app):
	valid_app_owner(app)

	editor_dir = get_app_editor_file_path(app)
	try:
		vf = open(os.path.join(editor_dir, "version"), 'r')
		if vf:
			version = vf.readline()
			vf.close()
		return int(version)

	except Exception:
		return


@frappe.whitelist()
def editor_worksapce_version(app):
	return editor_workspace_version(app)


@frappe.whitelist()
def editor_apply():
	from iot.device_api import send_action
	device = frappe.form_dict.device
	inst = frappe.form_dict.inst
	app = frappe.form_dict.app
	if not app or not inst or not device:
		raise frappe.ValidationError

	valid_app_owner(app)

	version = editor_workspace_version(app) or frappe.form_dict.version

	app_file = zip_application(app, version, True)
	os.system("md5sum " + app_file + " > " + app_file + ".md5")

	data = {
		"inst": inst,
		"name": app,
		"fork": 1,
		"version": "beta." + str(version) + ".editor"
	}
	return send_action("app", action="upgrade", device=device, data=data)


@frappe.whitelist()
def ping():
	return _("pong from app_center.editor.ping")
