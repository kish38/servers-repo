from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ServerType(models.Model):
    name = models.CharField(max_length=255)
    servers = models.IntegerField(default=0)
    vms = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name


class Server(models.Model):
    server_type = models.ForeignKey(ServerType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    ipv4_address = models.CharField(max_length=255)
    ipv6_address = models.CharField(max_length=255)
    idrac_ilo_ip = models.CharField(max_length=255)
    default_gateway = models.CharField(max_length=255)
    Dns_server_ip = models.CharField(max_length=255)
    storage = models.CharField(max_length=255)

    total_cups = models.CharField(max_length=255) 
    total_Sockets = models.CharField(max_length=255)
    cores_per_socket = models.CharField(max_length=255)
    threads_per_core = models.CharField(max_length=255)
    nics = models.CharField(max_length=255)
    cpu_average = models.CharField(max_length=255)
    memory = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=255)

    hard_drives_name = models.CharField(max_length=255)
    hard_model = models.CharField(max_length=255)
    hard_drives_size = models.CharField(max_length=255)

    os_version = models.CharField(max_length=255)
    kernel_version = models.CharField(max_length=255)
    uptime = models.CharField(max_length=255)
    
    vendor = models.CharField(max_length=255)
    server_model = models.CharField(max_length=255)
    cpu_series = models.CharField(max_length=255)
    bios_version = models.CharField(max_length=255)
    bios_release = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255)
    att_patch_level = models.CharField(max_length=255)
    running_vms = models.CharField(max_length=255)

    switch_info = models.JSONField(max_length=255)

    def __str__(self) -> str:
        return self.hardware_name


class Server1(models.Model):
    server_type = models.ForeignKey(ServerType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    hardware_name = models.CharField(max_length=255)
    cpu_model = models.CharField(max_length=255)
    memory = models.CharField(max_length=255)
    storage = models.CharField(max_length=255)
    network_info = models.CharField(max_length=255)
    firmware_version = models.CharField(max_length=255)
    power_cooling = models.CharField(max_length=255)
    cpu_utilisation = models.CharField(max_length=255)
    memory_usage = models.CharField(max_length=255)
    nics = models.CharField(max_length=255)
    load_average = models.CharField(max_length=255)
    os_version = models.CharField(max_length=255)

    hypervisor_details = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=255)
    mac_address = models.CharField(max_length=255)
    routing_tables = models.CharField(max_length=255)
    dns_dhp = models.CharField(max_length=255)
    switch_info = models.JSONField(max_length=255)
    idrac_ip = models.CharField(max_length=255)
    pxe_address = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.hardware_name


class Vm(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    vcpus = models.CharField(max_length=255)
    memory = models.CharField(max_length=255)
    disk_space = models.CharField(max_length=255)
    network_interface = models.CharField(max_length=255)
    guest_os = models.CharField(max_length=255)
    vcpu_utilisation = models.CharField(max_length=255)
    memory_usage = models.CharField(max_length=255)

    disk_io = models.CharField(max_length=255)
    load_average = models.CharField(max_length=255)
    io_wait = models.CharField(max_length=255)
    swap_usage = models.CharField(max_length=255)
    app_type = models.CharField(max_length=255)
    mots_id = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


@receiver(post_save, sender=Server)
def update_server_count(sender, instance, **kwargs):
    stype = instance.server_type
    stype.servers += 1
    stype.save()


@receiver(post_save, sender=Vm)
def update_vm_count(sender, instance, **kwargs):
    print(instance)
    print(instance.server)
    print(instance.server.server_type)
    stype = instance.server.server_type
    stype.vms += 1
    stype.save()


"""
['hardware name', 'cpu model', 'memory', 'storage', 'network info', 'firmware version', 'power cooling', 'cpu utilisation', 'load average', 'os version', 'hypervisor details', 'ip address', 'mac address', 'routing tables', 'dns dhp', 'switch info', 'idrac ip', 'pxe address', 'domain']
server,name,vcpus,memory,disk_space,network_interface,guest_os,vcpu_utilisation,memory_usage,disk_io,load_average,io_wait,swap_usage,app_type,mots_id
"""
