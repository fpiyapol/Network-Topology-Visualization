from django.db import models
from django.http import JsonResponse
# Create your models here.
class Management(models.Model):
    ip_addr = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    en_pass = models.CharField(max_length=255)

    def __str__(self):
        return self.ip_addr + ' ' + self.username

class Device(models.Model):
    hostname = models.CharField(max_length=255)
    device_type = models.CharField(max_length=1)
    
    def __str__(self):
        return self.hostname

class Interface(models.Model):
    device = models.ForeignKey(Device, related_name='interfaces', on_delete=models.CASCADE)
    port = models.CharField(max_length=255)
    ip_addr = models.CharField(max_length=255)
    n_hostname = models.CharField(max_length=255)
    n_interface = models.CharField(max_length=255)

    def __str__(self):
        return self.port + "|" + self.ip_addr + '|' + self.n_hostname + '|' + self.n_interface

class Link(models.Model):
    coord1 = models.CharField(max_length=255)
    coord2 = models.CharField(max_length=255)
    interface1 = models.CharField(max_length=255)
    interface2 = models.CharField(max_length=255)
