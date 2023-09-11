from django.db import models
from django.contrib.auth.models import User
from datetime import date

from django.urls.base import reverse

# Create your models here.
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    admin = models.BooleanField(null=False, default=False, help_text='True for admin, false otherwise')
    born = models.DateField(null=False, blank=False, help_text="Birth date")
    address = models.TextField(null=True, max_length=500, help_text="Full address")
    salary = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False, default=0.0, help_text="Monthly salary")

    @property
    def staff_id(self):
        return self.user.id
    
    @property
    def username(self):
        return self.user.username
    
    @property
    def email(self):
        return self.user.email

    @property
    def first_name(self):
        return self.user.first_name
    
    @first_name.setter
    def first_name(self, fname):
        if fname:
            self.user.first_name = fname
    
    @property
    def last_name(self):
        return self.user.last_name
    
    @last_name.setter
    def last_name(self, lname):
        if lname:
            self.user.last_name = lname
    
    @property
    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    @property
    def age(self):
        today = date.today()
        return today.year - self.born.year - ((today.month, today.day) < (self.born.month, self.born.day))
    
    def __str__(self):
        return self.username + '<' + self.email + '>'
    
    def get_absolute_url(self):
        return reverse('staff-detail', args=[str(self.staff_id)])
