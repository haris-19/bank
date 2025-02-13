from django.db import models

# Create your models here.
class Gender(models.Model):
    gender = models.CharField(max_length=7)
    
    def __str__(self):
        return self.gender
    
class State(models.Model):
    state= models.CharField(max_length=50)
    
    def __str__(self):
        return self.state
    

class Account(models.Model):
    name = models.CharField(max_length=32)
    Mobile_number= models.BigIntegerField()
    account_no = models.BigIntegerField()
    pin= models.IntegerField(blank=True, default=0)
    email = models.EmailField()
    aadhaar_card_no= models.PositiveIntegerField(unique=True)
    father_name = models.CharField(max_length=50)
    dob = models.DateField()
    address = models.CharField(max_length=1000)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=500)
    photo = models.ImageField(upload_to='profile_pics')
    
    def save(self, *args, **kwargs):
        if not self.account_no:
            last_account = Account.objects.order_by('-account_no').first()
            if last_account:
                self.account_no = last_account.account_no + 1
            else:
                self.account_no = 1234567890
        super().save(*args, **kwargs)
    