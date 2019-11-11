# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class IOTApplicationStatistics(Document):
	def after_insert(self):
		try:
			doc = frappe.get_doc("IOT Application Counter", self.app)
			doc.increase_installed()
		except:
			frappe.get_doc({
				"doctype": "IOT Application Counter",
				"app": self.app,
				"installed": 1
			}).insert()
