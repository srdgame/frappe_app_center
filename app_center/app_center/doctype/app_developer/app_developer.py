# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw,_
from frappe.model.document import Document


class AppDeveloper(Document):
	def after_insert(self):
		frappe.utils.user.add_role(self.user, 'App User')