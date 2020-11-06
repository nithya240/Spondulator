from django.contrib import admin

# Register your models here.
from .models import Cash, Purchase

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('my_user', 'stock', 'shares', 'price', 'bought_at')

admin.site.register(Cash)
admin.site.register(Purchase,PurchaseAdmin)
