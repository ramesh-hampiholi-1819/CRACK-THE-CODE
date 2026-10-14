from django.test import TestCase
from django.urls import reverse

from .models import Challenge, Language


class SitePagesTest(TestCase):
    def setUp(self):
        self.html = Language.objects.create(
            name='HTML',
            slug='html',
            tagline='Structure the web',
            description='Markup fundamentals.',
            color='#f97316',
            is_featured=True,
            order=1,
        )
        Challenge.objects.create(
            language=self.html,
            title='Hero Banner',
            slug='hero-banner',
            difficulty='Easy',
            description='Create a hero banner.',
            instructions='Create a basic landing block.',
            starter_code='<section></section>',
            example_input='',
            example_output='',
            constraints='Keep it simple.',
            hints='Use semantic tags.',
            is_featured=True,
            expected_output='hero',
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_languages_page_loads(self):
        response = self.client.get(reverse('languages'))
        self.assertEqual(response.status_code, 200)

    def test_language_detail_page_loads(self):
        response = self.client.get(reverse('language_detail', kwargs={'slug': 'html'}))
        self.assertEqual(response.status_code, 200)
