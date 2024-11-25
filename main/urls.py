from django.urls import path
from main.views import (
    index_view,
    login_view,
    logout_view
)


urlpatterns = [
    path('', index_view),
    path('login', login_view),
    path('logout', logout_view)
]
