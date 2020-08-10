# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.model.document import Document

class AppCenterSettings(Document):
	def validate(self):
		if self.enable_upper_center == 1:
			if self.iot_center is None:
				throw(_("Upper IOT Center is missing!"))
			if self.iot_center_auth_code is None:
				throw(_("Upper IOT Center Auth Code is missing!"))
			if self.on_behalf_developer is None:
				throw(_("On behalf developer is missing!"))

	def sync_app_center(self):
		if self.enable_upper_center != 1:
			throw(_("Upper Application Center is not enabled!"))

	def update_last_sync_time(self):
		self.last_sync_time = frappe.utils.now()
		self.save()