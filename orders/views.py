from rest_framework import viewsets, status
from rest_framework.response import Response

from simple_oms import settings
from .models import Customer, Order
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomerSerializer, OrderSerializer
from africastalking import initialize, SMS

# Initialize Africa's Talking
initialize(settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Call the parent's create method to create the order
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Get the customer associated with the order
        customer = order.customer  

        # Prepare and send the SMS
        if customer and customer.phone_number:  
            message = f"Thank you for your order! Your order ID is {order.id}."
            try:
                SMS.send(message, [customer.phone_number])
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
