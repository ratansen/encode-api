from django.db import models
import uuid,django
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Driver(models.Model):
    id = models.SlugField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(
        max_length=127)
    phone = PhoneNumberField(unique=True, )

    def __str__(self):
        return str(self.name)

class Bus(models.Model):
    id = models.SlugField(primary_key=True, default=uuid.uuid4)
    driver = models.ForeignKey(
        Driver, related_name='drivername', on_delete=models.CASCADE)
    
    destination_from = models.CharField(max_length=127)
    destination_to= models.CharField(
        max_length=127)
    
    date_of_departure = models.DateField(
        default=django.utils.timezone.now)
    time_of_departure = models.TimeField(
        default=django.utils.timezone.now)
    
    date_of_arrival = models.DateField(
        default=django.utils.timezone.now)
    time_of_arrival = models.TimeField(
        default=django.utils.timezone.now, help_text="Enter estimated time")

    def __str__(self):
        return str(self.destination_from+' '+'to'+' '+self.destination_to)
    
    

