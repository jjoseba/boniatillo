from django.contrib import admin

# Register your models here.
from currency.models import Entity, Category, Wallet

admin.site.register(Entity)
admin.site.register(Category)
admin.site.register(Wallet)