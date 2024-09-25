import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from oauth2_provider.models import Application
from django.contrib.auth.models import User

class CustomerTests(APITestCase):
    def setUp(self):
        # Create user and application for auth
        self.user = User.objects.create_user(username='admin', password='Admin123')
        self.application = Application.objects.create(
            name="simple_oms",
            redirect_uris="http://127.0.0.1:8000",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD
        )
# Get the user
user = User.objects.get(username="admin")

# Create the application object (but don't save yet)
app = Application(
    name="simple_oms",
    redirect_uris="http://127.0.0.1:8000",
    user=user,
    client_type=Application.CLIENT_CONFIDENTIAL,
    authorization_grant_type=Application.GRANT_PASSWORD, 
)

# Generate a plain-text client secret manually
from secrets import token_urlsafe
plain_client_secret = token_urlsafe(32)  

# Set the client_secret before saving
app.client_id = app.client_id
app.client_secret = plain_client_secret

# Save the application to the database
app.save()

print("Client ID:", app.client_id)
print("Client Secret (save this securely):", plain_client_secret)


app.save()

def get_token(self):
    url = "http://127.0.0.1:8000/o/token/"
    
    payload = {
        'grant_type': 'password',
        'username': 'admin',
        'password': 'Admin123',
        'client_id': app.client_id,
        'client_secret': app.client_secret
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(url, data=payload, headers=headers)
    
    # Print status and content for debugging
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content)
    
    return response.json()

def test_get_token(self):
    token_response = self.get_token()
    
    print("Token Response:", token_response)
    self.assertIn('access_token', token_response)

def test_create_customer(self):
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }
        # Customer data
        customer_data = {
            'name': 'Test Customer',
            'code': 'Test001',
            'phone_number': '1234567890',
        }
        # Use json parameter to send data
        response = self.client.post(reverse('customer-list'), json=customer_data, headers=headers)
        print("Response Data:", response.data)  # Debugging output
        print("Response Content:", response.content)  # Print raw response content for debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# def test_create_order(self):
#         headers = {
#             'Authorization': 'Bearer ' + self.token,
#             'Content-Type': 'application/json'
#         }
#         customer_response = self.client.post(reverse('customer-list'), 
#                                              json={'name': 'Test Customer',
#                                                     'code': 'Test001',
#                                                     'phone_number': '1234567890'}, 
#                                              headers=headers)
#         print("Customer Response Data:", customer_response.data)  # Debugging output
#         print("Customer Response Content:", customer_response.content)  # Print raw response content for debugging
#         self.assertEqual(customer_response.status_code, status.HTTP_201_CREATED)

#         # Check for customer ID
#         self.assertIn('id', customer_response.data)
        
#         # Order data
#         order_data = {
#             'customer': customer_response.data['id'],
#             'item': 'Sample Product',
#             'amount': 2,

#         }
#         order_response = self.client.post(reverse('order-list'), json=order_data, headers=headers)
#         print("Order Response Data:", order_response.data)  # Debugging output
#         print("Order Response Content:", order_response.content)  # Print raw response content for debugging
#         self.assertEqual(order_response.status_code, status.HTTP_201_CREATED)


