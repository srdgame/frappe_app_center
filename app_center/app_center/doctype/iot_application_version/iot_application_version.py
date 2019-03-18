# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.utils import now
from frappe.model.document import Document


class IOTApplicationVersion(Document):
	def validate(self):
		self.app_name = frappe.get_value('IOT Application', self.app, 'app_name')
		if self.is_new():
			latest = get_latest_version(self.app, 1)
			if latest >= int(self.version):
				throw(_("Version must be bigger than {0}").format(latest))

		"""
		if self.beta == 0:
			if self.tested == 1:
				throw(_("Cannot remove beta flag before tested!"))
			if self.approved == 1:
				throw(_("Cannot remove beta flag before approved!"))
		"""

	def autoname(self):
		self.name = self.app + "." + str(self.version)

	def before_save(self):
		if self.is_new():
			return

		if self.beta != 0:
			return

		org_beta = frappe.get_value("IOT Application Version", self.name, "beta")
		if org_beta == 0:
			return

		if int(self.version) > get_latest_version(self.app, 0):
			from app_center.appmgr import copy_to_latest
			copy_to_latest(self.app, self.version, 0)

	def on_trash(self):
		from app_center.appmgr import remove_version_file
		try:
			remove_version_file(self.app, self.version)
		except Exception as ex:
			frappe.logger(__name__).error(ex)

	def set_tested(self):
		self.set("tested", 1)
		self.set("tested_date", now())
		self.save()

	def set_approved(self):
		self.set("approved", 1)
		self.set("approved_date", now())
		self.save()


def on_doctype_update():
	"""Add indexes in `IOT Application Version`"""
	frappe.db.add_index("IOT Application Version", ["app", "version"])


def get_latest_version(app, beta=0):
	if int(beta) == 1:
		sql = "select max(version) from `tabIOT Application Version` where app='{0}'".format(app)
		return int(frappe.db.sql(sql)[0][0])
	else:
		sql = "select max(version) from `tabIOT Application Version` where app='{0}' and beta=0".format(app)
		return int(frappe.db.sql(sql)[0][0])

