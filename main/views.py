from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from main.models import ServerType, Server, Vm
import pandas as pd


server_columns = {
    "name": "name",
    "hardware name": "hardware_name",
    "cpu model": "cpu_model",
    "memory": "memory",
    "storage": "storage",
    "network info": "network_info",
    "firmware version": "firmware_version",
    "power cooling": "power_cooling",
    "cpu utilisation": "cpu_utilisation",
    "load average": "load_average",
    "os version": "os_version",
    "hypervisor details": "hypervisor_details",
    "ip address": "ip_address",
    "mac address": "mac_address",
    "routing tables": "routing_tables",
    "dns dhp": "dns_dhp",
    "switch info": "switch_info",
    "idrac ip": "idrac_ip",
    "pxe address": "pxe_address",
    "domain": "domain",
}
vm_columns = {
    "server": "server",
    "name": "name",
    "vcpus": "vcpus",
    "memory": "memory",
    "disk_space": "disk_space",
    "network_interface": "network_interface",
    "guest_os": "guest_os",
    "vcpu_utilisation": "vcpu_utilisation",
    "memory_usage": "memory_usage",
    "disk_io": "disk_io",
    "load_average": "load_average",
    "io_wait": "io_wait",
    "swap_usage": "swap_usage",
    "app_type": "app_type",
    "mots_id": "mots_id",
}


@login_required
def index_view(request):
    types = ServerType.objects.all()
    server_count = 0
    vms_count = 0
    for type1 in types:
        server_count += type1.servers
        vms_count += type1.vms

    return render(
        request,
        "index.html",
        {
            "server_types": types,
            "types_count": types.count(),
            "servers": server_count,
            "vms": vms_count,
        },
    )


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )
        if user:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid login details")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("/login")


def servers_view(request):
    servers = Server.objects.all()
    if "type" in request.GET:
        servers = servers.filter(server_type=request.GET["type"])
    return render(request, "server.html", {"servers": servers})


def vms_view(request):
    vms = Vm.objects.all()
    if "server" in request.GET:
        vms = vms.filter(server=request.GET["server"])
    return render(request, "vms.html", {"vms": vms})


def delete_server(request, id):
    server = Server.objects.filter(id=id).first()
    if server:
        stype = server.server_type
        stype.servers -= 1
        stype.vms -= Vm.objects.filter(server=server).count()
        server.delete()
        stype.save()

        messages.success(request, f"Deleted {server.name}")
    return redirect("/")


def delete_vm(request, id):
    server = Vm.objects.filter(id=id).first()
    if server:
        stype = server.server.server_type
        stype.vms -= 1
        server.delete()
        stype.save()
        messages.success(request, f"Deleted {server.name}")
    return redirect("/")


def search_view(request):
    if "key" not in request.GET:
        return redirect("/")
    key = request.GET['key'].strip()
    return render(request, 'search.html', {
        'servers': Server.objects.filter(name__contains=key),
        'vms': Vm.objects.filter(name__contains=key),
        'key': key
    })


def import_view(request):
    if request.method == "POST":
        sheets = pd.ExcelFile(request.FILES["excel_file"]).sheet_names
        if "servers" not in sheets or "vms" not in sheets:
            messages.error(request, "servers & vms sheets should be present in file")
            return redirect("/")
        servers_df = pd.read_excel(request.FILES["excel_file"], sheet_name="servers")
        vms_df = pd.read_excel(request.FILES["excel_file"], sheet_name="vms")

        for row in servers_df.to_dict("records"):
            stype = ServerType.objects.filter(name=row["type"]).first()
            if stype:
                del row["type"]
                try:
                    mrow = {v: row.get(k) for k, v in server_columns.items()}
                    server = Server(**mrow)
                    server.server_type = stype
                    server.save()
                except Exception as e:
                    print("Failed to add", row.get("name"), str(e))

        for row in vms_df.to_dict("records"):
            server = Server.objects.filter(name=row["server"]).first()
            if server:
                del row["server"]
                try:
                    mrow = {v: row.get(k) for k, v in vm_columns.items()}
                    vm = Vm(**mrow)
                    vm.server = server
                    vm.save()
                except Exception as e:
                    print("Failed to add", row.get("name"), str(e))
    else:
        messages.error(request, "Method not allowerd")
    return redirect("/")
