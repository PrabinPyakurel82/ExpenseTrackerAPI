from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import ExpenseIncome


class ExpenseIncomeTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="prabin", password="test123")
        login = self.client.post(reverse('token-obtain'), {
            'username': 'prabin',
            'password': 'test123'
        })
        self.access_token = login.data['access']
        self.refresh_token = login.data['refresh']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.admin = User.objects.create_superuser(username="admin", password="admin123")

    def test_register_user(self):
        res = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'test@example.com',
            'password': 'newpass123'
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_login_invalid_credentials(self):
        res = self.client.post(reverse('token-obtain'), {
            'username': 'wrong',
            'password': 'wrong'
        })
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        res = self.client.post(reverse('token-refresh'), {'refresh': self.refresh_token})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)

    def test_create_expense_flat_tax(self):
        res = self.client.post(reverse('expense-list'), {
            "title": "Groceries",
            "amount": "100.00",
            "transaction_type": "debit",
            "tax": "10.00",
            "tax_type": "flat"
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(res.data['total']), 110.0)

    def test_create_expense_percentage_tax(self):
        res = self.client.post(reverse('expense-list'), {
            "title": "Freelance",
            "amount": "200.00",
            "transaction_type": "credit",
            "tax": "10.00",
            "tax_type": "percentage"
        })
        self.assertEqual(float(res.data['total']), 220.0)

    def test_create_expense_zero_tax(self):
        res = self.client.post(reverse('expense-list'), {
            "title": "Gift",
            "amount": "100.00",
            "transaction_type": "credit",
            "tax": "0.00",
            "tax_type": "flat"
        })
        self.assertEqual(float(res.data['total']), 100.0)

    def test_list_own_expenses_only(self):
        self.test_create_expense_flat_tax()
        res = self.client.get(reverse('expense-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)

    def test_user_cannot_access_others_expense(self):
        self.test_create_expense_flat_tax()
        expense = ExpenseIncome.objects.first()

        user2 = User.objects.create_user(username='user2', password='pass123')
        login = self.client.post(reverse('token-obtain'), {
            'username': 'user2', 'password': 'pass123'
        })
        token = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        res = self.client.get(reverse('expense-detail', args=[expense.id]))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_access_all(self):
        self.test_create_expense_flat_tax()
        expense = ExpenseIncome.objects.first()

        login = self.client.post(reverse('token-obtain'), {
            'username': 'admin',
            'password': 'admin123'
        })
        token = login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        res = self.client.get(reverse('expense-detail', args=[expense.id]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_own_expense(self):
        self.test_create_expense_flat_tax()
        expense = ExpenseIncome.objects.first()
        url = reverse('expense-detail', args=[expense.id])
        res = self.client.put(url, {
            "title": "Updated Grocery",
            "amount": "120.00",
            "transaction_type": "debit",
            "tax": "10.00",
            "tax_type": "flat"
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(float(res.data['total']), 130.0)

    def test_delete_expense(self):
        self.test_create_expense_flat_tax()
        expense = ExpenseIncome.objects.first()
        url = reverse('expense-detail', args=[expense.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_access(self):
        self.client.credentials() 
        res = self.client.get(reverse('expense-list'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
