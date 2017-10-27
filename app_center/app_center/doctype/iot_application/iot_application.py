# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
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