from django.contrib import admin

# Register your models here.
from .models import Management, Device, Interface, Link

admin.site.register(Management)
admin.site.register(Device)
admin.site.register(Interface)
admin.site.register(Link)