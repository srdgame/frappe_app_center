# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class IOTApplicationFavorites(Document):
	def append_favorites(self, *favorites):

		"""Add favorite applications to list"""
		current_favorites = [d.app for d in self.get("favorites")]
		for fav in favorites:
			app = fav.get('app')
			comment = fav.get('comment')
			priority = fav.get('priority')

			if app in current_favorites:
				continue

			self.append("favorites", {"app": app, "comment": comment, "priority": priority})

	def add_favorites(self, *favorites):
		"""Add groups to favorite applications and save"""
		self.append_favorites(*favorites)
		self.save()

	def remove_favorites(self, *favorites):
		existing_favorites = dict((d.app, d) for d in self.get("favorites"))
		for app in favorites:
			if app in existing_favorites:
				self.get("favorites").remove(existing_favorites[app])

		self.save()
