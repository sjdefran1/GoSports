from django.urls import resolve
from django.test import TestCase
from GoSports.views import standings_tables

class UrlResolvesTest(TestCase):
    def test_root_url_resolves_to_standings_page_view(self):
        found = resolve('/standings/')
        self.assertEqual(found.func, standings_tables)


# Create your tests here.
