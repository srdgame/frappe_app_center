# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw
from frappe.model.document import Document


class AppDeveloperRequisition(Document):
	def validate(self):
		if self.docstatus == 0:
			if frappe.db.exists("App Developer", {"user": self.user}):
				throw("developer_exists")

			if frappe.db.exists("App Developer", {"nickname": self.nickname, "name": ('!=', self.name)}):
				throw("duplicated_developer_nickname")

			if frappe.db.exists("App Developer", {"id_card": self.id_card, "name": ('!=', self.name)}):
				throw("duplicated_developer_id_card")

		if frappe.db.exists("App Developer Requisition",
		                    {"nickname": self.nickname, "docstatus": ('!=', '1'), "name": ('!=', self.name)}):
			throw('duplicated_developer_nick_name')

		if frappe.db.exists("App Developer Requisition",
		                    {"id_card": self.id_card, "docstatus": ('!=', '1'), "name": ('!=', self.name)}):
			throw('duplicated_developer_id_card')

		if frappe.db.exists("App Developer Requisition",
		                    {"user": self.user, "docstatus": ('!=', '1'), "name": ('!=', self.name)}):
			throw('duplicated_developer_requisition')

	def on_submit(self):
		data = {
			"doctype": "App Developer",
			"user": self.user,
			"group": 'Normal',
			"nickname": self.domain,
			"id_card": self.id_card,
			"address": self.address,
			"pay_bank": self.pay_bank,
			"pay_account": self.pay_account,
			"enabled": 1
		}
		frappe.get_doc(data).insert()


