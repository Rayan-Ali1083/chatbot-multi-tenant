from django.db import models

# Create your models here.

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=255)
    collection_name = models.CharField(max_length=255, null=True)


    
class TenantAwareModel(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    
class Member(TenantAwareModel):
    
    name = models.CharField(max_length=255, unique=True)