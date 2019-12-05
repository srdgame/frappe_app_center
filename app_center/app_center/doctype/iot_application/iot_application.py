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
from six.moves.urllib.parse import quote
from cloud.cloud.doctype.cloud_company.cloud_company import list_user_companies


RESERVED_NAMES = ['skynet', 'skynet_iot', 'iot', 'freeioe', 'ioe', 'frpc', 'linux', 'ubuntu', 'debian', 'openwrt', 'admin', 'administrator']


class IOTApplication(Document):
	def autoname(self):
		if self.app_path or self.is_binary == 1:
			if not self.app_path:
				self.name = self._gen_app_path()
			else:
				self.name = self.app_path
		else:
			self.name = make_autoname('APP.########')

	def validate(self):
		if self.app_path and self.is_new():
			if frappe.session.user != 'Administrator':
				if self.app_path in RESERVED_NAMES:
					throw(_("Application path is not an valid path!"))
				if self.app_path.find("_skynet") >= 0:
					throw(_("Application path is not an valid path!"))

		""" Keep the app extension in lowercase """
		self.app_ext = self.app_ext.lower()

		if not self.developer and self.is_new():
			self.developer = frappe.session.user

		if self.company is not None:
			if self.company not in list_user_companies(self.developer):
				throw(_("You are not in company {0}".format(self.company)))

		""" Extension checking """
		if self.is_binary == 1:
			self.app_ext = "tar.gz"  # Extension must be tar.gz package.
			if not self.package_name:
				throw(_("Package name cannot be empty!"))
			if self.package_name != quote(self.package_name):
				throw(_("Package name invalid!!!"))
			if not self.os_system:
				throw(_("OS System cannot be empty!"))
			if not self.os_version:
				throw(_("OS Version cannot be empty!"))
			if not self.hw_arch:
				throw(_("IOT Hardware Architecture cannot be empty!"))
			self.app_path = self._gen_app_path()
			self.code_name = None
		else:
			""" Validate code name """
			if self.code_name != quote(self.code_name):
				throw(_("Application code name invalid!!!"))

			self.code_name = secure_filename(self.code_name or self.app_name).replace(' ', '_')
			if self.code_name.find('.') >= 0:
				throw(_("Application code name cannot include dot character(.)!"))

		""" If Application is not binary application correct app_path """
		if self.is_new():
			""" Generate the path when not administrator and not binary"""
			if self.is_binary == 0 and frappe.session.user != 'Administrator':
				self.app_path = self._gen_app_path()

			if not self.app_path and frappe.session.user == 'Administrator':
				if self.developer != frappe.session.user:
					self.app_path = self._gen_app_path()

			self.app_name_unique = self._gen_app_uinque()

	def _gen_app_uinque(self):
		if self.is_binary == 1:
			return self.app_path
		else:
			return self.developer if self.company is None else self.company + "/" + self.code_name

	def _gen_app_path(self):
		if self.is_binary == 1:
			arch = frappe.get_value("IOT Hardware Architecture", self.hw_arch, "arch")
			return "bin/{0}/{1}/{2}/{3}".format(self.os_system, self.os_version, arch, self.package_name)

		if self.company is not None:
			domain = frappe.get_value("Cloud Company", self.company, "domain")
			return domain + "/" + (self.code_name or secure_filename(self.app_name).replace(' ', '_'))

		# Generate app_path by nick_name/app_code_name
		dev_nick_name = frappe.get_value("App Developer", self.developer, 'nickname')
		if dev_nick_name:
			return dev_nick_name + "/" + (self.code_name or secure_filename(self.app_name).replace(' ', '_'))

	def before_save(self):
		if not self.is_new():
			org_path = frappe.get_value("IOT Application", self.name, 'app_path')
			if org_path != self.app_path:
				if org_path:
					update_app_link(self.name, org_path, self.app_path)
				else:
					create_app_link(self.name, self.app_path)

	def before_insert(self):
		if frappe.session.user == 'Administrator':
			return
		applist = frappe.db.get_values('IOT Application', {"developer": self.developer})
		group = frappe.get_value("App Developer", self.developer, "group")
		if len(applist) >= 10 and group == 'Normal':
			throw(_("Application count limitation!"))
		if len(applist) >= 20 and group == 'Power':
			throw(_("Application count limitation!"))
		if len(applist) >= 100 and group == 'Admin':
			throw(_("Application count limitation!"))

	def after_insert(self):
		create_app_link(self.name, self.app_path)

	def on_trash(self):
		from app_center.appmgr import remove_app_folder
		try:
			remove_app_link(self.app_path)
			remove_app_folder(self.app)
		except Exception as ex:
			frappe.logger(__name__).error(ex)

	def get_fork(self, developer, version):
		return frappe.get_value('IOT Application', {"fork_from": self.name, "fork_version": version, "developer": developer}, "name")

	def fork(self, by_user, version, pre_conf=None):
		if self.is_binary == 1:
			throw(_("Extension cannot be forked!!!"))

		if self.get_fork(by_user, version):
			throw(_("You have already forked {0} version {1}").format(self.app_name, version))
		data = {
			"doctype": "IOT Application",
			"app_name": self.app_name + "." + str(version),
			"code_name": self.code_name + "_fork_with_" + str(version),
			"developer": by_user,
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
			"has_conf_template": self.has_conf_template,
			"conf_template": self.conf_template,
			"pre_configuration": pre_conf or self.pre_configuration,
			"published": 0
		}
		doc = frappe.get_doc(data).insert()

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