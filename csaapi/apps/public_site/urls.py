from django.urls import include, path, register_converter


from apps.common import converters, views


register_converter(converters.ULIDConverter, "ulid")
app_name = "apps.api"


urlpatterns = []
