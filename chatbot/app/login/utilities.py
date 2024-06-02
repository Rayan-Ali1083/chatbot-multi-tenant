from .models import Tenant

def get_hostname(request):
    hostname = request.get_host().split(':')[0].lower()
    print(f'Hostname: {hostname}')
    return hostname


def get_tenant(request):
    hostname = get_hostname(request)
    subdomain = hostname.split('.')[0]
    print(f'Subdomain: {subdomain}')
    return Tenant.objects.filter(subdomain=subdomain).first()