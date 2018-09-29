from django.test import TestCase
from lists.models import Item
from django.urls import resolve # resolve是django内部函数，用于解析url，并将其映射到相应的视图函数
from django.http import HttpRequest
from django.template.loader import render_to_string #render_to_string将模板渲染成str
from lists.views import home_page
# Create your tests here.

class HomePageTest(TestCase):
	def test_uses_home_template(self):	# 不是测试视图函数返回的常量，而是测试视图函数实现方式
		response = self.client.get('/lists/') # self.client是django提供的测试客户端
		self.assertTemplateUsed(response, 'lists/home.html') # 只能判断通过self.client获取的响应
	
	def test_can_save_a_POST_request(self):
		response = self.client.post('/lists/', data={'item_text': 'A new list item'})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
		self.assertIn('A new list item', response.content.decode())
		self.assertTemplateUsed(response, 'lists/home.html')
	
	def test_only_saves_items_when_necessary(self):
		'''只保存非空待办事项'''
		self.client.get('/lists/')
		self.assertEqual(Item.objects.count(), 0)
		

class ItemModelTest(TestCase):
	
	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()
		
		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()
		
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item' )
		self.assertEqual(second_saved_item.text, 'Item the second')
		
		
		