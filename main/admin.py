from django.contrib import admin
from main.models import *


class ServerAdmin(admin.ModelAdmin):
    list_display = ("server_type", "name", "memory", "storage", "ip_address")


class VmAdmin(admin.ModelAdmin):
    list_display = ("server", "name", "vcpus", "memory", "disk_space", "mots_id")


admin.site.register(ServerType)
admin.site.register(Server, ServerAdmin)
admin.site.register(Vm, VmAdmin)
