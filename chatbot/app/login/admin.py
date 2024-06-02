from django.contrib import admin

# Register your models here.

from .models import Tenant, Member

admin.site.register(Tenant)
admin.site.register(Member)