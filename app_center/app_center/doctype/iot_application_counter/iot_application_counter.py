# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document


class IOTApplicationCounter(Document):
	def increase_installed(self):
		self.installed = self.installed + 1
		self.save(ignore_permissions=True, ignore_version=True)