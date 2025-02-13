from django.contrib import admin
from .models import Account,Gender, State
# Register your models here.
admin.site.register(Account)
admin.site.register(Gender)
admin.site.register(State)