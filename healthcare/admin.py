from django.contrib import admin
from .models import  Notification, Medications, Patient

admin.site.register(Patient)
admin.site.register(Notification)
admin.site.register(Medications)