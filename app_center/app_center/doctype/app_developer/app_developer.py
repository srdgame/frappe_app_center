# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw,_
from frappe.model.document import Document


class AppDeveloper(Document):
	# def validate(self):
	# 	if self.alias.find('@') >= 0:
	# 		throw(_("Developer Alias cannot include character @"))
	pass