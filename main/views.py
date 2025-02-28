from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from main.models import ServerType, Server, Vm
import pandas as pd
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from copy import deepcopy


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
        scount = Server.objects.filter(server_type=type1).count()
        vcount = Vm.objects.filter(server__server_type=type1).count()
        server_count += scount
        vms_count += vcount
        type1.servers = scount
        type1.vms = vcount

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


def add_server_view(request):
    if request.method == 'POST':
        dct = {}
        for k in request.POST:
            dct[k] = request.POST[k]
        stype = ServerType.objects.get(id=dct['stype'])
        name = dct['hardware_name']
        del dct['csrfmiddlewaretoken']
        del dct['stype']
        server = Server(**dct)
        server.name = name
        server.server_type = stype
        server.save()
        return redirect("/servers")
    stypes = ServerType.objects.all()
    return render(request, 'addserver.html', {'stypes': stypes})


def add_vm_view(request):
    if request.method == 'POST':
        dct = {}
        for k in request.POST:
            dct[k] = request.POST[k]
        server = Server.objects.get(id=dct['server'])
        dct['server'] = server
        del dct['csrfmiddlewaretoken']
        vm = Vm(**dct)
        vm.save()
        return redirect("/vms")
    return render(request, 'addvms.html', {'servers': Server.objects.all()})


def edit_server_view(request, id):
    server = Server.objects.get(id=id)
    cols = server_columns.values()
    server_dct = {}
    for col in cols:
        server_dct[col] = getattr(server, col)
    server_dct['stype'] = server.server_type.id
    if request.method == 'POST':
        if request.POST['stype'] != server_dct['stype']:
            server.server_type = ServerType.objects.get(id=request.POST['stype'])

        for k in request.POST:
            if k not in ['csrfmiddlewaretoken', 'stype']:
                setattr(server, k, request.POST[k])
        server.save()
        return redirect(f"/edit-server/{id}")
    return render(request, 'addserver.html', {'server_id': id, 'stypes': ServerType.objects.all(), 'data': json.dumps(server_dct)})


def edit_vm_view(request, id):
    server = Vm.objects.get(id=id)
    cols = vm_columns.values()
    server_dct = {}
    for col in cols:
        server_dct[col] = getattr(server, col)
    server_dct['server'] = server.server.id
    if request.method == 'POST':
        if request.POST['server'] != server_dct['server']:
            server.server = Server.objects.get(id=request.POST['server'])

        for k in request.POST:
            if k not in ['csrfmiddlewaretoken', 'server']:
                setattr(server, k, request.POST[k])
        server.save()
        return redirect(f"/edit-vm/{id}")
    return render(request, 'addvms.html', {'vm_id': id, 'servers': Server.objects.all(), 'data': json.dumps(server_dct)})


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


@csrf_exempt
def add_vm_req(request):
    if request.method == "GET":
        return JsonResponse({"error": "GET /create-vm not found"})
    data = json.loads(request.body)
    vm = Vm.objects.filter(name=data['VM Name']).first()
    if 'server_name' in data:
        server = Server.objects.filter(name=data.get('server_name', '')).first()
        if not server:
            return JsonResponse({"error": "Invalid server name"})
    elif vm:
        server = vm.server
    else:
        server = Server.objects.first()
    vm_dct = {key: '' for key in vm_columns}
    vm_dct['server'] = server
    vm_dct['name'] = data['VM Name']
    vm_dct['vcpus'] = data['CPU']
    vm_dct['memory'] = data['RAM']
    vm_dct['guest_os'] = data['OS']
    if not vm:
        vm = Vm.objects.create(**vm_dct)
    else:
        Vm.objects.filter(pk=vm.pk).update(**vm_dct)
    return JsonResponse({"success": "VM Created"})


@csrf_exempt
def add_server_req(request):
    if request.method == "GET":
        return JsonResponse({"error": "GET /create-server not found"})
    data = json.loads(request.body)
    server = Server.objects.filter(name=data['host']).first()
    # if 'server_name' in data:
    #     server = Server.objects.filter(name=data.get('server_name', '')).first()
    #     if not server:
    #         return JsonResponse({"error": "Invalid server name"})
    # elif vm:
    #     server = vm.server
    # else:
    #     server = Server.objects.first()
    server_dct = {key: '' for key in server_columns}
    server_dct['cpu_model'] = data['server_bios'].get('CPU Model')
    server_dct['memory'] = data['hardware'].get('Total RAM')
    server_dct["cpu_utilisation"] = data['hardware'].get('CPU Average')
    server_dct["memory_usage"] = data['hardware'].get('Memory Average')
    server_dct["nics"] = data['hardware'].get('NICs')
    server_dct['os_version'] = data['operating_system'].get('OS')
    server_dct['ip_address'] = data['network'].get('IPv4 Address')
    server_dct['idrac_ip'] = data['network'].get('iDRAC/iLO IP Address')
    server_dct['switch_info'] = json.dumps({'switches': data['lldp_switches']})

    server_dct['mac_address'] = data['server_bios'].get('Server Serial Number')
    server_dct['firmware_version'] = data['operating_system'].get('Kernel Version')
    server_dct['network_info'] = json.dumps(data['network'])

    server_dct['server_type'] = ServerType.objects.get(name='Arcadian')


    if not server:
        server = Server.objects.create(**server_dct)
    else:
        Server.objects.filter(pk=server.pk).update(**server_dct)
    return JsonResponse({"success": "Server Created"})


def get_server_req(request, id):
    server = Server.objects.get(id=id)
    return render(request, 'serverdetails.html', {'server': server})