#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file_name：'tests.py '
author：'baobinghuan'
create_time：'2018/9/26'
"""
from django.test import LiveServerTestCase # LiveServerTestCase是django提供创建测试数据库，并开启服务，让功能测试在其中运行
from selenium import webdriver
from selenium.webdriver.common.keys import  Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10
class NewVisitorTest(LiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
	
	def tearDown(self):
		self.browser.quit()
	
	def wait_for_row_in_list_table(self,row_text):
		'''用于等待的辅助函数，重试循环，轮询应用，尽早向前行进'''
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except(AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)
				
	
	def test_can_start_a_list_for_one_user(self):
		self.browser.get(f'{self.live_server_url}/lists')
		self.assertIn('To-Do lists', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		# 输入待办事
		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')
		input_box.send_keys('Buy peacock feathers')
		# 按回车，页面刷新保存
		input_box.send_keys(Keys.ENTER)
		# 待办事项表格显示
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		# 继续显示输入框
		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(input_box.get_attribute('placeholder'),'Enter a to-do item')
		input_box.send_keys('Use peacock feathers to make a fly')
		# 按回车，页面刷新保存
		input_box.send_keys(Keys.ENTER)
		# 待办事项表格显示两个待办事项
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
		
		# 网站是否保存了待办事项
		# 网站为待办事项生成了唯一的url
		# 页面有些文字解说这一功能
		# 访问待办事项列表的url，待办事项清单还在
		# 满意，睡觉
	
	def test_multiple_users_can_start_lists_at_different_urls(self):
		'''不同用户生成不同的待办事项清单urls'''
		self.browser.get(f'{self.live_server_url}/lists')
		self.assertIn('To-Do lists',self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do',header_text)
		# 输入待办事
		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(input_box.get_attribute('placeholder'),'Enter a to-do item')
		input_box.send_keys('Buy peacock feathers')
		# 按回车，页面刷新保存
		input_box.send_keys(Keys.ENTER)
		# 待办事项表格显示
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		
		# 伊迪斯的待办事项清单有唯一url
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+') # unittest提供的辅助函数，检查字符串是否匹配正则表达式
		
		# 弗朗西斯访问网站
		## 确保旧用户信息cookies不会泄露，使用新的浏览器会话
		self.browser.quit()
		self.browser = webdriver.Firefox()
		
		#  访问首页看不到旧用户的待办事项清单
		self.browser.get(f'{self.live_server_url}/lists')
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly',page_text)
		
		# 新用户输入待办事项，新建一个清单
		input_box = self.browser.find_element_by_id('id_new_item')
		input_box.send_keys('Buy milk')
		input_box.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		
		# 弗朗西斯获得他的唯一url
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)
		
		# 创建弗朗西斯清单成功后返回的页面依然没有伊迪斯的清单
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)
		
		# 两人都很满意，都去睡觉了
	
	
		
		

