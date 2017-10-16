# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
import redis
import uuid
from frappe import throw, msgprint, _


@frappe.whitelist()
def new_app():
	if frappe.request.method != "POST":
		throw(_("Request Method Must be POST!"))
	filename = frappe.form_dict.file
	print(filename)
	print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')

