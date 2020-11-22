from django.contrib import admin

from application.models import ApplicationByDispatcher, ApplicationByCommissioner, PhotoForApplicationByCommissioner, \
    Decision, RefusalOfApplicationByDispatcher


@admin.register(ApplicationByDispatcher)
class ApplicationByDispatcherAdmin(admin.ModelAdmin):
    readonly_fields = ['number']
    list_filter = ['commissioner', 'point']
    ordering = ['-created_at']

@admin.register(PhotoForApplicationByCommissioner)
class PhotoForApplicationByCommissionerAdmin(admin.ModelAdmin):
    pass

class PhotoForApplicationByCommissionerInLine(admin.TabularInline):
    model = PhotoForApplicationByCommissioner
    extra = 0


@admin.register(ApplicationByCommissioner)
class ApplicationByCommissionerAdmin(admin.ModelAdmin):
    readonly_fields = ['number']
    list_filter = ['commissioner', 'point']
    ordering = ['-created_at']
    inlines = [
        PhotoForApplicationByCommissionerInLine
    ]


@admin.register(Decision)
class DecisionAdmin(admin.ModelAdmin):
    list_filter = ['dispatcher']
    ordering = ['-created_at']


@admin.register(RefusalOfApplicationByDispatcher)
class DecisionAdmin(admin.ModelAdmin):
    readonly_fields = ['commissioner', 'comment', 'created_at']
    list_filter = ['commissioner']
    ordering = ['-created_at']