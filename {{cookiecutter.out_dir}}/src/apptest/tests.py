# -*- coding: utf-8 -*-
import unittest

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse


class ConfigTestCase(TestCase):

    def test_default_language(self):
        """
        Most of the time, this is this language we want.
        """
        self.assertEqual(settings.LANGUAGE_CODE, 'fr-fr')

    def test_default_timezone(self):
        """
        Most of the time, this is the timezone we want, not UTC.
        """
        self.assertEqual(settings.TIME_ZONE, 'Europe/Paris')


@unittest.skipIf(
    'apptest' not in settings.INSTALLED_APPS,
    'You MUST copy/paste {{cookiecutter.django_project_name}}.settings.local.py.dist and add '
    'apptest in INSTALLED_APPS'
)
class AppTestTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url_hello = reverse('apptest:helloworld')

    @override_settings(LANGUAGE_CODE='fr-fr')
    def test_hello_world_translation_default_fr(self):
        """
        Most of the time, we code app in English and then translate it in
        French. But in real life, there is no use at all for English. Worst, we
        make wrong translation, just like me :-). It is better to write it in
        our favorite language and then translate it.

        So we make sure that without translation, we use raw string which are
        in French, my native language and probably yours too!
        """
        response = self.client.get(self.url_hello)
        self.assertContains(response, 'Salut')

    @override_settings(LANGUAGE_CODE='en-us')
    def test_hello_world_translation_en(self):
        """
        On contrary, be sure that English translation is used.
        """
        response = self.client.get(self.url_hello)
        self.assertContains(response, 'Hello')
