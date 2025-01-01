from django.contrib import admin
from .models import User_reg, Transactions, Supports

# User Data Model
admin.site.register(User_reg)

# Transaction Data Model
admin.site.register(Transactions)

# Support Data Model
admin.site.register(Supports)