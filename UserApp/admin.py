from django.contrib import admin
from .models import Payment
# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("card_no","cvv","expiry","balance")

admin.site.register(Payment,PaymentAdmin)
