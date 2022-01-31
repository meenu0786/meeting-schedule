from django.contrib import admin
from .models import Schedule, NonUser
from django.apps import apps

admin.site.register(Schedule)
admin.site.register(NonUser)
# Register your models here.

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)
