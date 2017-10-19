# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class IOTApplicationVersion(Document):
	def validate(self):
		self.app_name = frappe.get_value('IOT Application', self.app, 'app_name')

	def autoname(self):
		self.name = self.app + "." + str(self.version)

	def on_trash(self):
		from app_center.api import app_remove
		try:
			app_remove(self.app, self.version)
		except Exception as ex:
			frappe.logger(__name__).error(ex.message)