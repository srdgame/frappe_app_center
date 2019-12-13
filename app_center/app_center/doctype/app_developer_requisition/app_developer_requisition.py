# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import re
from frappe import throw
from frappe.model.document import Document
from app_center.app_center.doctype.app_developer.app_developer import check_id_card

match_dev_name = re.compile(r'([a-z]\w+)', re.I)


class AppDeveloperRequisition(Document):
	def validate(self):
		m = match_dev_name.match(self.dev_name)
		if not m:
			throw('invalid_nick_name')
		dev_name_g = m.groups()
		if len(dev_name_g) == 0:
			throw('invalid_nick_name')
		if dev_name_g[0] != self.dev_name:
			throw('invalid_nick_name')

		valid, err = check_id_card(self.id_card)
		if not valid:
			throw(err)

		if self.docstatus == 0:
			if frappe.db.exists("App Developer", {"user": self.user}):
				throw("developer_exists")

			if frappe.db.exists("App Developer", {"dev_name": self.dev_name, "name": ('!=', self.name)}):
				throw("duplicated_developer_name")

			if frappe.db.exists("App Developer", {"id_card": self.id_card, "name": ('!=', self.name)}):
				throw("duplicated_developer_id_card")

		if frappe.db.exists("App Developer Requisition",
		                    {"dev_name": self.dev_name, "docstatus": ('!=', '1'), "name": ('!=', self.name)}):
			throw('duplicated_developer_name')

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
			"dev_name": self.dev_name,
			"id_name": self.id_name,
			"id_card": self.id_card,
			"address": self.address,
			"pay_bank": self.pay_bank,
			"pay_account": self.pay_account,
			"enabled": 1
		}
		frappe.get_doc(data).insert()


