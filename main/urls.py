from django.urls import path
from main.views import (
    index_view,
    login_view,
    logout_view,
    servers_view,
    vms_view,
    import_view,
    search_view,
    delete_server,
    delete_vm,
    add_server_view,
    add_vm_view,
    edit_server_view,
    edit_vm_view
)


urlpatterns = [
    path("", index_view),
    path("login", login_view),
    path("logout", logout_view),
    path("servers", servers_view),
    path("vms", vms_view),
    path("import", import_view),
    path("search", search_view),
    path("delete-server/<int:id>", delete_server),
    path("delete-vm/<int:id>", delete_vm),
    path("add-server", add_server_view),
    path("add-vm", add_vm_view),
    path("edit-server/<int:id>", edit_server_view),
    path("edit-vm/<int:id>", edit_vm_view)
]
