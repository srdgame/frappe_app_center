# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Developers"),
			"items": [
				{
					"type": "doctype",
					"name": "App Developer",
					"onboard": 1,
					"description": _("App Developer"),
				},
				{
					"type": "doctype",
					"name": "App Developer Requisition",
					"onboard": 1,
					"description": _("App Developer Requisition"),
				},
			]
		},
		{
			"label": _("Application Center"),
			"items": [
				{
					"type": "doctype",
					"name": "IOT Application",
					"onboard": 1,
					"description": _("IOT Application"),
				},
				{
					"type": "doctype",
					"name": "IOT Application Version",
					"onboard": 1,
					"description": _("IOT Application Version"),
				},
				{
					"type": "doctype",
					"name": "IOT Application Review",
					"onboard": 1,
					"description": _("IOT Application Review"),
				},
				{
					"type": "doctype",
					"name": "IOT Application Comment",
					"onboard": 1,
					"description": _("IOT Application Comment"),
				},
				{
					"type": "doctype",
					"name": "IOT Application Issue",
					"onboard": 1,
					"description": _("IOT Application Issue"),
				}
			]
		},
		{
			"label": _("Statistics"),
			"items": [
				{
					"type": "doctype",
					"name": "IOT Application Counter",
					"onboard": 1,
					"description": _("IOT Application Counter"),
				},
				{
					"type": "doctype",
					"name": "IOT Application Statistics",
					"onboard": 1,
					"description": _("IOT Application Statistics"),
				},
				{
					"type": "doctype",
					"name": "IOT Application Favorites",
					"onboard": 1,
					"description": _("IOT Application Favorites"),
				}
			]
		},
		{
			"label": _("Settings"),
			"items": [
				{
					"type": "doctype",
					"name": "App Center Settings",
					"onboard": 1,
					"description": _("App Center Settings"),
				},
				{
					"type": "doctype",
					"name": "App Category",
					"onboard": 1,
					"description": _("App Category"),
				},
				{
					"type": "doctype",
					"name": "IOT Hardware Architecture",
					"onboard": 1,
					"description": _("IOT Hardware Architecture"),
				},
				{
					"type": "doctype",
					"name": "App Center Child Node",
					"onboard": 1,
					"description": _("App Center Child Node"),
				}
			]
		}
	]
