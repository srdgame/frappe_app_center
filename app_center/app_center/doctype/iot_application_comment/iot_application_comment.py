# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class IOTApplicationComment(Document):
	def on_trash(self):
		for d in frappe.db.get_values("IOT Application Comment", {"reply_to": self.name}, "name"):
			frappe.delete_doc("IOT Application Conf", d[0])
