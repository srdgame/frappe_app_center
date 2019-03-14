# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import time
import os
import json
from frappe import throw, _
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import get_files_path
from werkzeug.utils import secure_filename


RESERVED_NAMES = ['skynet_iot', 'iot']


class IOTApplication(Document):
	def autoname(self):
		if self.app_path:
			self.name = self.app_path
		else:
			self.name = make_autoname('APP.########')
			self.app_path = self._gen_app_path()

	def validate(self):
		if self.app_path and self.is_new():
			if frappe.session.user != 'Administrator':
				if self.app_path in RESERVED_NAMES:
					throw(_("Application path is not an valid path!"))
				if self.app_path.find("_skynet") >= 0:
					throw(_("Application path is not an valid path!"))

		self.code_name = secure_filename(self.code_name or self.app_name).replace(' ', '_')
		if self.code_name.find('.') >= 0:
			throw(_("Application code name cannot include dot character(.)!"))
		self.app_ext = self.app_ext.lower()
		self.app_name_unique = self.owner + "/" + self.code_name
		if self.name != self.app_path:
			self.app_path = self._gen_app_path()

	def _gen_app_path(self):
		dev_nick_name = frappe.get_value("App Developer", self.owner, 'nickname')
		if dev_nick_name:
			return dev_nick_name + "/" + (self.code_name or secure_filename(self.app_name).replace(' ', '_'))

	def before_save(self):
		if self.is_new():
			create_app_link(self.name, self.app_path)
		else:
			org_path = frappe.get_value("IOT Application", self.name, 'app_path')
			if org_path != self.app_path:
				if org_path:
					update_app_link(self.name, org_path, self.app_path)
				else:
					create_app_link(self.name, self.app_path)

	def before_insert(self):
		if frappe.session.user == 'Administrator':
			return
		applist = frappe.db.get_values('IOT Application', {"owner": self.owner})
		group = frappe.get_value("App Developer", self.owner, "group")
		if len(applist) >= 10 and group == 'Normal':
			throw(_("Application count limitation!"))
		if len(applist) >= 20 and group == 'Power':
			throw(_("Application count limitation!"))
		if len(applist) >= 100 and group == 'Admin':
			throw(_("Application count limitation!"))

	def on_trash(self):
		from app_center.appmgr import remove_app_folder
		try:
			remove_app_link(self.app_path)
			remove_app_folder(self.app)
		except Exception as ex:
			frappe.logger(__name__).error(ex)

	def get_fork(self, owner, version):
		return frappe.get_value('IOT Application', {"fork_from": self.name, "fork_version": version, "owner": owner}, "name")

	def fork(self, by_user, version, pre_conf=None):
		if self.get_fork(by_user, version):
			throw(_("You have already forked {0} version {1}").format(self.app_name, version))
		data = {
			"doctype": "IOT Application",
			"app_name": self.app_name + "." + str(version),
			"code_name": self.code_name,
			"owner": by_user,
			"license_type": self.license_type,
			"fork_from": self.name,
			"fork_version": version,
			"fork_track": 1,
			"description": self.description,
			"category": self.category,
			"device_supplier": self.device_supplier,
			"device_serial": self.device_serial,
			"protocol": self.protocol,
			"app_ext": self.app_ext,
			"pre_configuration": pre_conf or self.pre_configuration,
			"published": 0
		}
		doc = frappe.get_doc(data).insert()

		# Copy keywords
		keywords = [d.key for d in self.get("keywords")]
		if len(keywords) > 0:
			doc.add_keywords(keywords)

		return doc

	def update_stars(self):
		if not self.has_permission("write"):
			raise frappe.PermissionError

		try:
			sql = "select avg(star) from `tabIOT Application Review` where app='{0}'".format(self.name)
			star = float(frappe.db.sql(sql)[0][0])
			self.set("star", star)
		except Exception as ex:
			self.set("start", 0)

		self.save()

	def update_app_path(self):
		if not self.code_name:
			self.code_name = secure_filename(self.app_name).replace(' ', '_')

		if self.name != self.app_path:
			app_path = self._gen_app_path()
			if app_path == self.app_path:
				self.save()
				return

		create_app_link(self.name, self.app_path, force=False)

	def clean_before_delete(self):
		if not self.has_permission("write"):
			raise frappe.PermissionError

		for d in frappe.db.get_values("IOT Application Version", {"app": self.name}, "name"):
			frappe.delete_doc("IOT Application Version", d[0])

		for d in frappe.db.get_values("IOT Application Comment", {"app": self.name}, "name"):
			frappe.delete_doc("IOT Application Comment", d[0])

		for d in frappe.db.get_values("IOT Application Issue", {"app": self.name}, "name"):
			for d1 in frappe.db.get_values("IOT Application IssueReview", {"parent": d[0]}, "name"):
				frappe.delete_doc("IOT Application IssueReview", d1[0])
			frappe.delete_doc("IOT Application Issue", d[0])

		for d in frappe.db.get_values("IOT Application Review", {"app": self.name}, "name"):
			for d1 in frappe.db.get_values("IOT Application ReviewComment", {"parent": d[0]}, "name"):
				frappe.delete_doc("IOT Application iot_application_reviewcomment", d1[0])
			frappe.delete_doc("IOT Application Review", d[0])

		for d in frappe.db.get_values("IOT Application Conf", {"app": self.name}, "name"):
			doc = frappe.get_doc("IOT Application Conf", d[0])
			doc.clean_before_delete()
			frappe.delete_doc("IOT Application Conf", d[0])

	def append_keywords(self, *keywords):
		"""Add groups to user"""
		current_keywords = [d.key for d in self.get("keywords")]
		for key in keywords:
			if key in current_keywords:
				continue
			self.append("keywords", {"key": key})

	def add_keywords(self, *keywords):
		"""Add groups to user and save"""
		self.append_keywords(*keywords)
		self.save()

	def remove_keywords(self, *keywords):
		existing_keywords = dict((d.key, d) for d in self.get("keywords"))
		for key in keywords:
			if key in existing_keywords:
				self.get("keywords").remove(existing_keywords[key])
		self.save()


def get_recently_apps(as_list=False):
	"""Returns a count of incomplete todos"""
	data = frappe.get_list("IOT Application",
		fields=["name", "description"] if as_list else "count(*)",
		filters=[["ToDo", "status", "=", "Open"]],
		or_filters=[["ToDo", "owner", "=", frappe.session.user],
			["ToDo", "assigned_by", "=", frappe.session.user]],
		as_list=True)

	if as_list:
		return data
	else:
		return data[0][0]


def update_stars(app):
	time.sleep(3)
	doc = frappe.get_doc("IOT Application", app)
	doc.update_stars()


def get_app_unique_path(app_path):
	basedir = get_files_path('app_center_files')
	package_dir = os.path.join(basedir, 'packages')
	if not os.path.exists(package_dir):
		os.makedirs(package_dir)

	unique_path = os.path.join(package_dir, app_path)
	base_dir = os.path.dirname(unique_path)
	if not os.path.exists(base_dir):
		os.makedirs(base_dir)

	return unique_path


def create_app_link(app, app_path, force=True):
	from app_center.appmgr import get_app_release_path
	src_path = os.path.realpath(get_app_release_path(app))
	link_path = os.path.realpath(get_app_unique_path(app_path))

	if src_path == link_path:
		return

	if os.path.exists(link_path):
		if not force:
			return
		else:
			os.remove(link_path)

	os.symlink(src_path, link_path)


def remove_app_link(app_path):
	link_path = get_app_unique_path(app_path)
	if os.path.exists(link_path):
		os.remove(link_path)


def update_app_link(app, org_path, new_path):
	create_app_link(app, new_path)
	remove_app_link(org_path)


def update_package_owner(org_nickname, new_nickname):
	basedir = get_files_path('app_center_files')
	package_dir = os.path.join(basedir, 'packages')
	if not os.path.exists(package_dir):
		os.makedirs(package_dir)

	org_dir = os.path.join(package_dir, org_nickname)
	if not os.path.exists(org_dir):
		return
	os.rename(org_dir, os.path.join(package_dir, new_nickname))


@frappe.whitelist()
def update_apps_path(names, status=None):
	if not frappe.has_permission("IOT Application", "write"):
		frappe.throw(_("Not permitted"), frappe.PermissionError)

	names = json.loads(names)
	for name in names:
		doc = frappe.get_doc("IOT Application", name)
		doc.update_app_path()


@frappe.whitelist()
def update_apps_stars(names, status=None):
	if not frappe.has_permission("IOT Application", "write"):
		frappe.throw(_("Not permitted"), frappe.PermissionError)

	names = json.loads(names)
	for name in names:
		doc = frappe.get_doc("IOT Application", name)
		doc.update_stars()


def list_tags(app):
	return []


def add_tags(app, *tags):
	return tags


def remove_tags(app, *tags):
	return []


def clear_tags(app):
	return []
