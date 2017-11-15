# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import time
from frappe import throw, _
from frappe.model.document import Document
from frappe.model.naming import make_autoname

RESERVED_NAMES = ['skynet_iot', 'iot']


class IOTApplication(Document):
	def autoname(self):
		if self.app_path:
			self.name = self.app_path
		else:
			#self.name = self.owner + "." + self.app_name
			self.name = make_autoname('APP.########')

	def validate(self):
		if self.app_path:
			if self.app_path.find('.') >= 0:
				throw(_("Application path cannot include dot character(.)!"))
			if frappe.session.user != 'Administrator':
				if self.app_path in RESERVED_NAMES:
					throw(_("Application path is not an valid path!"))
				if self.app_path.find("_skynet") >= 0:
					throw(_("Application path is not an valid path!"))
		self.app_ext = self.app_ext.lower()
		self.app_name_unique = self.owner + "/" + self.app_name

	def before_insert(self):
		applist = frappe.db.get_values('IOT Application', {"owner": self.owner})
		group = frappe.get_value("App Developer", self.owner, "group")
		if len(applist) > 10 and group == 'Normal':
			throw(_("Application count limitation!"))
		if len(applist) > 20 and group == 'Power':
			throw(_("Application count limitation!"))
		if len(applist) > 100 and group == 'Admin':
			throw(_("Application count limitation!"))

	def on_trash(self):
		from app_center.appmgr import remove_app_folder
		try:
			remove_app_folder(self.app)
		except Exception as ex:
			frappe.logger(__name__).error(ex.message)

	def get_fork(self, owner, version):
		return frappe.get_value('IOT Application', {"fork_from": self.name, "fork_version": version}, "name")

	def fork(self, by_user, version):
		if self.get_fork(by_user, version):
			throw(_("You have already forked {0} version {1}").format(self.app_name, version))
		data = {
			"doctype": "IOT Application",
			"app_name": self.app_name + "." + str(version),
			"owner": by_user,
			"license_type": self.license_type,
			"fork_from": self.name,
			"fork_version": version,
			"description": self.description,
			"category": self.category,
			"device_supplier": self.device_supplier,
			"device_serial": self.device_serial,
			"protocol": self.protocol,
			"app_ext": self.app_ext,
		}
		return frappe.get_doc(data).insert()

	def update_stars(self):
		sql = "select avg(star) from `tabIOT Application Review` where app='{0}'".format(self.name)
		star = float(frappe.db.sql(sql)[0][0])
		self.set("star", star)
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
