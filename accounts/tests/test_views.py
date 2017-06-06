from django.test import TestCase

from tickets.tests import factories as tickets_factories

from accounts.models import User


class ProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.alice = User.objects.create_user(email_addr='alice@example.com', name='Alice')

    def setUp(self):
        self.client.force_login(self.alice)

    def test_get_profile_when_not_authenticated(self):
        self.client.logout()
        rsp = self.client.get('/profile/', follow=True)
        self.assertRedirects(rsp, '/accounts/login/?next=/profile/')

    def test_get_profile_with_no_ticket(self):
        rsp = self.client.get('/profile/')
        self.assertContains(rsp, '<a href="/tickets/orders/new/">Buy one now!</a>', html=True)

    def test_get_profile_with_ticket(self):
        tickets_factories.create_ticket(self.alice)

        rsp = self.client.get('/profile/')
        self.assertNotContains(rsp, '<a href="/tickets/orders/new/">Buy one now!</a>', html=True)
        self.assertContains(rsp, 'You have a ticket for Thursday, Friday, Saturday')


class RegisterTests(TestCase):
    def test_success(self):
        data = {
            'name': 'Alice',
            'email_addr': 'alice@example.com',
            'password1': 'Pa55w0rd',
            'password2': 'Pa55w0rd',
        }
        rsp = self.client.post('/accounts/register/', data, follow=True)
        self.assertContains(rsp, 'Hello, Alice')

    def test_password_mismatch(self):
        data = {
            'name': 'Alice',
            'email_addr': 'alice@example.com',
            'password1': 'Pa55w0rd',
            'password2': 'Pa55wOrd',
        }
        rsp = self.client.post('/accounts/register/', data, follow=True)
        self.assertContains(rsp, "The two password fields didn&#39;t match")

    def test_password_too_short(self):
        data = {
            'name': 'Alice',
            'email_addr': 'alice@example.com',
            'password1': 'pw',
            'password2': 'pw',
        }
        rsp = self.client.post('/accounts/register/', data, follow=True)
        self.assertContains(rsp, 'This password is too short')

    def test_email_taken(self):
        tickets_factories.create_user('Alice')
        data = {
            'name': 'Alice',
            'email_addr': 'alice@example.com',
            'password1': 'Pa55w0rd',
            'password2': 'Pa55w0rd',
        }
        rsp = self.client.post('/accounts/register/', data, follow=True)
        self.assertContains(rsp, 'That email address has already been registered')