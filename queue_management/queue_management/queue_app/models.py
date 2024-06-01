from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class QueueEntry(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    invited = models.BooleanField(default=False)
    served = models.BooleanField(default=False)
    desk = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.timestamp}"
class CustomerVisit(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)