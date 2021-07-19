""" CSA Demo API URL Configuration """

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


from rest_framework_simplejwt import views as jwt_views


from apps.api import urls as api_urls, views as api_views


api_urls = []

app_urls = [
    path("", include("django.contrib.auth.urls")),
    path("", include("apps.common.urls", namespace="common")),
    path("", include("apps.farm_site.urls", namespace="farm")),
    path("", include("apps.member_site.urls", namespace="member")),
    path("", include("apps.public_site.urls", namespace="public")),
    path("", include("apps.users.urls", namespace="users")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(api_urls)),
    path("", include(app_urls)),
]


admin.site.site_header = "CSA Demo API Administration"
admin.site.site_title = "CSA Demo API Administration"
admin.site.index_title = "CSA Demo API Administration"
