from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.item} - {self.amount}'
