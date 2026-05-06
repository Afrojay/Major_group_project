from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from glossary.views import StaffLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/login/",
        StaffLoginView.as_view(),
        name="login",
    ),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("glossary.urls")),
]
