
# imports
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# User Model
class User_reg(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.IntegerField(default=0)
    account_number = models.CharField(max_length=20,unique=True)
    email = models.EmailField(max_length=30)
    gender = models.CharField(max_length=20)
    account_type = models.CharField(max_length=40)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.CharField(max_length=500,default="")
    image = models.ImageField(upload_to="User/Images",default="",null=True)
    Pan = models.CharField(max_length=50,default="")
    aadhaar = models.CharField(max_length=50,default="")
    DoB = models.CharField(max_length=20,default="")
    

    def __str__(self):
        return self.user.username

# Transaction Model    
class Transactions(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
        ('TRANSFER', 'Transfer')
    ]

    user = models.ForeignKey(User_reg,on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20,choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(default=timezone.now())
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    about = models.CharField(max_length=100)
    receiptent = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    receiptent_no = models.CharField(max_length=30, default="",null=True)

    def __str__(self):
        return self.user.user.username

# Support Model    
class Supports(models.Model):

    name = models.CharField(max_length=20,default="")
    email = models.EmailField(max_length=40)
    issue = models.CharField(max_length=300,default="")

    def __str__(self):
        return self.name