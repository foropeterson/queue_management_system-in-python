from django.contrib import admin
from .models import Customer, QueueEntry

admin.site.register(Customer)
admin.site.register(QueueEntry)
