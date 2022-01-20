# Create your tests here.
from django.test import SimpleTestCase
from django.test import TestCase, Client
from django.urls import reverse
from Discussions.models import *
from Accounts.models import *
import json

class TestViews(TestCase):
    def test_project_home_get(self):
        client = Client()
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Discussions/home.html')


class TestWrongViews(TestCase):
    def test_project_wrong_get(self):
        client = Client()
        response = self.client.get(reverse('wrong'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Discussions/wrong.html')


class TopicTestCase(TestCase):
    def setUp(self):
        Topic.objects.create(name="MyTestTopic")

    def test_topics_can_speak(self):
        topic = Topic.objects.get(name="MyTestTopic")
        self.assertEqual(topic.name, 'MyTestTopic')


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="pranta123", email="pranta123@gmail.com", password="user1234")

    def test_user_can_speak(self):
        user = User.objects.get(username="pranta123")
        self.assertEqual(user.username, 'pranta123')