from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from SEapp.models import Product
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken


class ProductApiTest(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Temporary product', price=1.99, available=True)
        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', kwargs={'pk': self.product.id})
        self.client = APIClient()
        self.regular_user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin = User.objects.create_superuser(username='testadmin', password='testpassword')

    def authenticate_user(self, user):
        token = str(AccessToken.for_user(user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_get_all_products(self):
        self.authenticate_user(self.regular_user)
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.authenticate_user(self.admin)
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_product(self):
        self.authenticate_user(self.regular_user)
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.authenticate_user(self.admin)
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_product_with_valid_data(self):
        data = {"name": "Temporary Product 2", "price": 4.99, "available": True}

        self.authenticate_user(self.regular_user)
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.authenticate_user(self.admin)
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Temporary Product 2')

    def test_modify_existing_product_with_valid_data(self):
        data = {"name": "Modified Product"}

        self.authenticate_user(self.regular_user)
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.authenticate_user(self.admin)
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Modified Product')

    def test_delete_existing_product(self):
        self.authenticate_user(self.regular_user)
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.authenticate_user(self.admin)
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_create_new_product_with_invalid_data(self):
        invalid_data = {"name": "", "price": -10, "available": "invalid_value"}

        self.authenticate_user(self.admin)
        response = self.client.post(self.product_list_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertIn("price", response.data)
        self.assertIn("available", response.data)

    def test_modify_product_with_invalid_data(self):
        invalid_data = {"price": "invalid_price"}

        self.authenticate_user(self.admin)
        response = self.client.patch(self.product_detail_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)

    def test_access_product_list_without_authentication(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_product_detail_without_authentication(self):
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_endpoint(self):
        invalid_url = "/invalid-endpoint/"
        self.authenticate_user(self.admin)
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_product(self):
        nonexistent_url = reverse('product-detail', kwargs={'pk': 999})
        self.authenticate_user(self.admin)
        response = self.client.delete(nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product_without_required_fields(self):
        data = {"price": 3.99}

        self.authenticate_user(self.admin)
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_modify_product_with_empty_data(self):
        empty_data = {}

        self.authenticate_user(self.admin)
        response = self.client.patch(self.product_detail_url, empty_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_unauthorized_delete_attempt(self):
        self.authenticate_user(self.regular_user)
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_product_as_regular_user(self):
        data = {"name": "Regular User Product", "price": 3.99, "available": True}

        self.authenticate_user(self.regular_user)
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
