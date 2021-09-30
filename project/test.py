from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from project.models import Statistic
from source.constants import API_SECURE_KEY

header = {'HTTP_API-SECURE-KEY': '%s' % API_SECURE_KEY}


class ServiceTest(TestCase):
    def test_success_save_statistic(self):
        data = {'date': '2021-12-20', 'views': 0, 'clicks': 0, 'cost': 10.5}
        response = self.client.post(path=reverse('save_statistic'), data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('result'), "SUCCESSFULLY_ADDED_STATISTIC")

    def test_fail_save_statistic(self):
        data = {'date': '2021.12.20', 'views': 0, 'clicks': 0, 'cost': 10.5}
        response = self.client.post(path=reverse('save_statistic'), data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('result').get('date')[0],
                         "Неправильный формат date. Используйте один из этих форматов: YYYY-MM-DD.")

    def test_delete_all_statistic(self):
        Statistic.objects.create(date='2021-01-12')
        Statistic.objects.create(date='2021-01-13')
        response = self.client.delete(path=reverse('delete_statistic'), **header)
        self.assertEqual(response.status_code, status.HTTP_410_GONE)
        self.assertEqual(response.json().get('result'), "STATISTIC_SUCCESSFULLY_DELETED")

    def test_delete_if_not_statistic(self):
        response = self.client.delete(path=reverse('delete_statistic'), **header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json().get('result'), "NO_STATISTIC")

    def test_get_statistic_out_of_date_range(self):
        Statistic.objects.create(date='2021-09-12', views=1000, clicks=120, cost=50)
        Statistic.objects.create(date='2021-09-19', views=500, clicks=50, cost=100)
        data = {'from': '2021-09-20', 'to': '2021-09-30'}
        response = self.client.get(path=reverse('get_statistic'), data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json().get('result'), "NO_DATA")

    def test_get_statistic_one_in_date_range(self):
        Statistic.objects.create(date='2021-09-12', views=1000, clicks=120, cost=50)
        Statistic.objects.create(date='2021-09-19', views=500, clicks=50, cost=100)
        data = {'from': '2021-09-13', 'to': '2021-09-19'}
        response = self.client.get(path=reverse('get_statistic'), data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('result')), 1)

    def test_get_statistic_two_in_date_range(self):
        Statistic.objects.create(date='2021-09-12', views=1000, clicks=120, cost=50)
        Statistic.objects.create(date='2021-09-19', views=500, clicks=50, cost=100)
        data = {'from': '2021-09-12', 'to': '2021-09-19'}
        response = self.client.get(path=reverse('get_statistic'), data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('result')), 2)

    def test_get_statistic_with_wrong_date_value(self):
        Statistic.objects.create(date='2021-09-12', views=1000, clicks=120, cost=50)
        Statistic.objects.create(date='2021-09-19', views=500, clicks=50, cost=100)
        data = {'from': '2021.09.12', 'to': '2021.09.19'}
        response = self.client.get(path=reverse('get_statistic'), data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('date')[0],
                         "Неправильный формат date. Используйте один из этих форматов: YYYY-MM-DD.")

    def test_get_statistic_without_date_value(self):
        Statistic.objects.create(date='2021-09-12', views=1000, clicks=120, cost=50)
        Statistic.objects.create(date='2021-09-19', views=500, clicks=50, cost=100)
        data = {}
        response = self.client.get(path=reverse('get_statistic'), data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('result'), "NO_OR_WRONG_FIELDS_from_AND_to")

    def test_get_statistic_sorted_every_field(self):
        Statistic.objects.create(date='2021-09-12', views=1000, clicks=120, cost=50)
        Statistic.objects.create(date='2021-09-19', views=500, clicks=50, cost=100)
        sort_field = ['date', 'views', 'clicks', "cost", "cpc", "cpm"]
        for field in sort_field:
            data = {'from': '2021-09-12', 'to': '2021-09-19', 'sort_by_field': field}
            response = self.client.get(path=reverse('get_statistic'), data=data, **header)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            sorted_data = sorted(response.json().get('result'), key=lambda k: k[field], reverse=True)
            self.assertEqual(response.json().get('result'), sorted_data)

    def test_get_statistic_sorted_with_wrong_sort_field(self):
        Statistic.objects.create(date='2021-09-12', views=1000, clicks=120, cost=50)
        Statistic.objects.create(date='2021-09-19', views=500, clicks=50, cost=100)
        data = {'from': '2021-09-12', 'to': '2021-09-19', 'sort_by_field': 'dates'}
        response = self.client.get(path=reverse('get_statistic'), data=data, **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('result'), "SORT_FIELD_ERROR")
