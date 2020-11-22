from django.contrib import admin
from django.contrib.auth.models import User

from users.models import Commissioner, Dispatcher


@admin.register(Commissioner)
class CommissionerAdmin(admin.ModelAdmin):
    exclude = ['user']

    def save_model(self, request, obj, form, change):
        user = User.objects.create(username=f'{obj.first_name} {obj.surname} {obj.phone}')
        obj.user = user
        super(CommissionerAdmin, self).save_model(request, obj, form, change)


@admin.register(Dispatcher)
class DispatcherAdmin(admin.ModelAdmin):
    exclude = ['user']

    def save_model(self, request, obj, form, change):
        user = User.objects.create(username=f'{obj.first_name} {obj.surname} {obj.phone}')
        obj.user = user
        super(DispatcherAdmin, self).save_model(request, obj, form, change)
