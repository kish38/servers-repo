from django.db import models


class ServerType(models.Model):
    name = models.CharField(max_length=255)
    servers = models.IntegerField(default=0)
    vms = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name


class Server(models.Model):
    hardware_name = models.CharField(max_length=255)
    cpu_model = models.CharField(max_length=255)
    memory = models.CharField(max_length=255)
    storage = models.CharField(max_length=255)
    network_info = models.CharField(max_length=255)
    firmware_version = models.CharField(max_length=255)
    power_cooling = models.CharField(max_length=255)
    cpu_utilisation = models.CharField(max_length=255)
    load_average = models.CharField(max_length=255)
    os_version = models.CharField(max_length=255)

    hypervisor_details = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=255)
    mac_address = models.CharField(max_length=255)
    routing_tables = models.CharField(max_length=255)
    dns_dhp = models.CharField(max_length=255)
    switch_info = models.CharField(max_length=255)
    idrac_ip = models.CharField(max_length=255)
    pxe_address = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.hardware_name


'''
['hardware name', 'cpu model', 'memory', 'storage', 'network info', 'firmware version', 'power cooling', 'cpu utilisation', 'load average', 'os version', 'hypervisor details', 'ip address', 'mac address', 'routing tables', 'dns dhp', 'switch info', 'idrac ip', 'pxe address', 'domain']
'''