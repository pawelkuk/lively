from django.shortcuts import redirect
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver


class UserViewTestCase(TestCase):

    def setUp(self):
        self.username = 'myuser'
        self.password = 'Secure_123'
        self.client = Client()
        self.url = reverse('user_home')
        User.objects.create_user(self.username, 'hereisanemail@test.com', self.password)

    def test_home_view_redirects_unauthenticated_user_to_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/user/login/?next=/user/')

    # def test_home_view_redirects_authenticated_user_to_home(self):
    #     self.client.login(username=self.username, password=self.password)
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, reverse('user_home'))


class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.username = 'myuser'
        self.password = 'Secure_123'
        self.user = User.objects.create_user(self.username, 'hereisanemail@test.com', self.password)

    def login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/user/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(self.user.username)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(self.password)
        self.selenium.find_element_by_css_selector('body > div > form > button').click()
