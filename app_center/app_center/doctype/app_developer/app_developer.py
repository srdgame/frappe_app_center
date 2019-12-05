# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import re
from frappe import throw, _
from frappe.utils.user import add_role
from frappe.model.document import Document
from six.moves.urllib.parse import quote


class AppDeveloper(Document):
	def validate(self):
		if self.nickname != quote(self.nickname):
			throw(_("Invalid Nickname!!!"))

		if frappe.session.user != 'Administrator' and len(self.nickname) < 6:
			throw(_("Nickname cannot be less than six characters!"))

		if frappe.session.user != 'Administrator' and frappe.get_value("App Developer", {"id_card": self.id_card, "name": ('!=', self.name)}, "name"):
			throw(_("id_card_duplicated_with_others!"))

		if self.nickname.find('.') >= 0:
			throw(_("Nickname cannot include dot character(.)!"))

		if self.nickname.find('/') >= 0:
			throw(_("Nickname cannot include dot character(/)!"))

		if self.nickname in ['bin', 'admin', 'ext', 'openwrt', 'linux', 'lede', 'ioe', 'freeioe', 'thingsroot', 'administrator', 'user']:
			throw(_("Invalid Nickname!!!!!!"))

		valid, err = check_id_card(self.id_card)
		if not valid:
			throw(err)

	def after_insert(self):
		add_role(self.user, 'App User')

	def before_save(self):
		org_nickname = frappe.get_value("App Developer", self.name, "nickname")
		if not org_nickname:
			for d in frappe.db.get_values("IOT Application", {"developer": self.name}, "name"):
				doc = frappe.get_doc("IOT Application", d[0])
				doc.update_app_path()

		if org_nickname is not None and org_nickname != self.nickname:
			from app_center.app_center.doctype.iot_application.iot_application import update_package_owner
			update_package_owner(org_nickname, self.nickname)


# Errors=['验证通过!','身份证号码位数不对!','身份证号码出生日期超出范围或含有非法字符!','身份证号码校验错误!','身份证地区非法!']
def check_id_card(id_card):
	# errors = ['验证通过!', '身份证号码位数不对!', '身份证号码出生日期超出范围或含有非法字符!', '身份证号码校验错误!', '身份证地区非法!']
	errors = ['valid_ok', 'invalid_id_card_length', 'invalid_birth_date', 'invalid_check_sum', 'invalid_region']
	area = {"11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古", "21": "辽宁", "22": "吉林", "23": "黑龙江",
			"31": "上海", "32": "江苏", "33": "浙江", "34": "安徽", "35": "福建", "36": "江西", "37": "山东", "41": "河南", "42": "湖北",
			"43": "湖南", "44": "广东", "45": "广西", "46": "海南", "50": "重庆", "51": "四川", "52": "贵州", "53": "云南", "54": "西藏",
			"61": "陕西", "62": "甘肃", "63": "青海", "64": "宁夏", "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门", "91": "国外"}
	id_card = str(id_card)
	id_card = id_card.strip()
	id_card_list = list(id_card)

	if not area[id_card[0:2]]: # 地区校验
		return False, errors[4]

	if len(id_card) == 15: # 15位身份号码检测
		if (int(id_card[6:8]) + 1900) % 4 == 0 or (
				(int(id_card[6:8]) + 1900) % 100 == 0 and (int(id_card[6:8]) + 1900) % 4 == 0):
			re_id = re.compile(
				'[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$')  # //测试出生日期的合法性
		else:
			re_id = re.compile(
				'[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$')  # //测试出生日期的合法性
		if re.match(re_id, id_card):
			return True, errors[0]
		else:
			return False, errors[2]
	elif len(id_card) == 18:  # 18位身份号码检测
		# 出生日期的合法性检查
		# 闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
		# 平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
		if int(id_card[6:10]) % 4 == 0 or (int(id_card[6:10]) % 100 == 0 and int(id_card[6:10]) % 4 == 0):
			re_id = re.compile(
				'[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$')  # //闰年出生日期的合法性正则表达式
		else:
			re_id = re.compile(
				'[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$')  # //平年出生日期的合法性正则表达式
		# //测试出生日期的合法性
		if re.match(re_id, id_card):
			# //计算校验位
			S = (int(id_card_list[0]) + int(id_card_list[10])) * 7 + (int(id_card_list[1]) + int(id_card_list[11])) * 9 + (
						int(id_card_list[2]) + int(id_card_list[12])) * 10 + (
							int(id_card_list[3]) + int(id_card_list[13])) * 5 + (
							int(id_card_list[4]) + int(id_card_list[14])) * 8 + (
							int(id_card_list[5]) + int(id_card_list[15])) * 4 + (
							int(id_card_list[6]) + int(id_card_list[16])) * 2 + int(id_card_list[7]) * 1 + int(
				id_card_list[8]) * 6 + int(id_card_list[9]) * 3
			Y = S % 11
			JYM = "10X98765432"
			M = JYM[Y]  # 判断校验位
			if M == id_card_list[17]:  # 检测ID的校验位
				return True, errors[0]
			else:
				return False, errors[3]
		else:
			return False, errors[2]
	else:
		return False, errors[1]