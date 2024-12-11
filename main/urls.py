from django.urls import path
from main.views import (
    index_view,
    login_view,
    logout_view,
    servers_view,
    vms_view,
    import_view,
    search_view
)


urlpatterns = [
    path("", index_view),
    path("login", login_view),
    path("logout", logout_view),
    path("servers", servers_view),
    path("vms", vms_view),
    path("import", import_view),
    path("search", search_view)
]
