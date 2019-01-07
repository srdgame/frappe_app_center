# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw,_
from frappe.utils.user import add_role
from frappe.model.document import Document
from six.moves.urllib.parse import quote


class AppDeveloper(Document):
	def validate(self):
		if self.nickname != quote(self.nickname):
			throw(_("Invalid Nickname!!!"))

	def after_insert(self):
		add_role(self.user, 'App User')

	def before_save(self):
		org_nickname = frappe.get_value("App Developer", self.name, "nickname")
		if not org_nickname:
			for d in frappe.db.get_values("IOT Application", {"owner": self.name}, "name"):
				doc = frappe.get_doc("IOT Application", d[0])
				doc.save()

		if org_nickname is not None and org_nickname != self.nickname:
			from app_center.app_center.doctype.iot_application.iot_application import update_package_owner
			update_package_owner(org_nickname, self.nickname)

