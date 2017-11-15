# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class IOTApplicationReview(Document):
	def on_update(self):
		frappe.enqueue('app_center.app_center.doctype.iot_application.iot_application.update_stars', app=self.app)

	def on_trash(self):
		frappe.enqueue('app_center.app_center.doctype.iot_application.iot_application.update_stars', app=self.app)
