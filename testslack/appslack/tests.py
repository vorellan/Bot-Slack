from __future__ import unicode_literals
from django.test import TestCase, Client
from .views import *
from .models import *


class TestClient(TestCase):

    def setUp(self):
        self.url = reverse_lazy('post', current_app='appcshopslack')

    def test_homepage_when_client_call_it_then_return_200(self):
        client = Client()
        homepage = client.get('/menu/list')
        self.assertEqual(homepage.status_code, 200)

    def test_agenda__when_client_call_it_then_return_200(self):
        client = Client()
        homepage = client.get('/menu/agenda')
        self.assertEqual(homepage.status_code, 200)

    def test_user_list_when_client_call_it_then_return_200(self):
        client = Client()
        homepage = client.get('/menu/userlist')
        self.assertEqual(homepage.status_code, 200)

    def test_urls_when_client_call_it_and_not_exist_then_return_200(self):
        client = Client()
        homepage = client.get('/menu/fakepage')
        self.assertEqual(homepage.status_code, 404)

    def test_post_when_token_is_invalid_then_return_403(self):
        client = Client()
        data = {'token': 'CixZEOtYA7t6SO'}
        response = client.post('/menu/slack', data=data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_post_when_type_is_valid_then_return_200(self):
        client = Client()
        data = {'token': 'CixZEOtYA7t6SO9CrmLtLqj1',
                'type': 'url_verification'}
        response = client.post('/menu/slack', data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_post_when_menu_today_is_not_exist_then_not_found_and_return_204(self):
        client = Client()
        data = {'token': 'CixZEOtYA7t6SO9CrmLtLqj1'}
        response = client.post('/menu/slack', data=data, format='json')
        menu_yesterday = Menu(opcion1='Pollo', opcion2='Empanadas', opcion3='Sopa', opcion4='Ensalada', fecha='2018-10-08')
        menu_yesterday.save()
        query_menu_today = Menu.objects.filter(fecha='2018-10-09')
        query_count = query_menu_today.count()
        self.assertEqual(query_count, 0)
        self.assertEqual(response.status_code, 204)

    def test_post_when_menu_today_exist_then_send_a_message_to_slack_and_return_202(self):
        now_date = datetime.datetime.now().date()
        menu = Menu(opcion1='Pollo', opcion2='Empanadas', opcion3='Sopa', opcion4='Ensalada', fecha=now_date)
        menu.save()
        client = Client()
        data = {'token': 'CixZEOtYA7t6SO9CrmLtLqj1'}
        response = client.post('/menu/slack', data=data, format='json')
        self.assertEqual(response.status_code, 202)


class TestModel(TestCase):

    def setUp(self):
        self.menu = Menu(opcion1='Pollo', opcion2='Empanadas', opcion3='Sopa', opcion4='Ensalada',fecha='2018-06-07')
        self.client = Cliente(id='1-k', nombre='Juan')

    def test_menu_model_when_add_new_menu_then_create_it(self):
        first_count = Menu.objects.count()
        self.menu.save()
        second_count = Menu.objects.count()
        self.assertNotEqual(first_count, second_count)

    def test_cliente_model_when_add_new_client_then_create_it(self):
        first_count = Cliente.objects.count()
        self.client.save()
        second_count = Cliente.objects.count()
        self.assertNotEqual(first_count, second_count)

    def test_menu_model_when_delete_item_then_delete_it(self):
        self.menu.save()
        first_count = Menu.objects.count()
        self.menu.delete()
        second_count = Menu.objects.count()
        self.assertNotEqual(first_count, second_count)

    def test_cliente_model_when_delete_item_then_delete_it(self):
        self.client.save()
        first_count = Cliente.objects.count()
        self.client.delete()
        second_count = Cliente.objects.count()
        self.assertNotEqual(first_count, second_count)
