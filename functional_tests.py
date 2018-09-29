#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file_name：'functional_tests.py '
author：'baobinghuan'
create_time：'2018/9/26'
"""
from selenium import webdriver
from selenium.webdriver.common.keys import  Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
	
	def tearDown(self):
		self.browser.quit()
	
	def check_for_row_in_list_table(self,row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])
	
	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get('http://localhost:8000/lists')
		self.assertIn('To-Do lists', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		# 输入待办事
		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')
		input_box.send_keys('Buy peacock feathers')
		# 按回车，页面刷新保存
		input_box.send_keys(Keys.ENTER)
		time.sleep(1)
		# 待办事项表格显示
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		# 继续显示输入框
		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(input_box.get_attribute('placeholder'),'Enter a to-do item')
		input_box.send_keys('Use peacock feathers to make a fly')
		# 按回车，页面刷新保存
		input_box.send_keys(Keys.ENTER)
		time.sleep(1)
		# 待办事项表格显示两个待办事项
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
		
		# 网站是否保存了待办事项
		# 网站为待办事项生成了唯一的url
		# 页面有些文字解说这一功能
		
		self.fail('Finish the test!')



if __name__ == "__main__":
	unittest.main(warnings='ignore')
	