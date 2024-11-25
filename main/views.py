from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from main.models import ServerType, Server


@login_required
def index_view(request):
    types = ServerType.objects.all()
    server_count = 0
    vms_count = 0
    for type1 in types:
        server_count += type1.servers
        vms_count += type1.vms

    return render(request, 'index.html', {
        'server_types': types,
        'types_count': types.count(),
        'servers': server_count,
        'vms': vms_count
    })


def login_view(request):
    if request.method == "POST":
        print(request.POST)
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )
        print(user)
        if user:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid login details")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("/login")