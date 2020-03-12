import frappe

# This patch set the developer value from owner field


def execute():
	frappe.reload_doc('conf_center', 'doctype', 'iot_application')
	table_columns = frappe.db.get_table_columns("IOT Application")
	if not table_columns:
		return

	if "developer" in table_columns:
		frappe.db.sql('''
			update `tabIOT Application`
			set developer = owner
			where ifnull(developer, '') = ''
		''')
		frappe.db.sql('''
			update `tabIOT Application`
			set developer = owner
			where developer = '\n'
		''')

	frappe.clear_cache()

	# for name in frappe.db.sql_list("select name from `tabIOT Application` where ifnull(developer, '')!=''"):
	# 	try:
	# 		doc = frappe.get_doc("IOT Application", name)
	# 		if doc.developer is None or len(doc.developer) == 0 or doc.developer == '\n':
	# 			doc.developer = doc.owner
	# 			doc.save()
	# 	except Exception as e:
	# 		if not frappe.db.is_table_missing(e):
	# 			raise