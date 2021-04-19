from django.contrib import admin

from logs.models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['ip', 'date', 'method', 'uri', 'status_code', 'size']
    list_filter = ['method', 'status_code', 'date', 'created']
    search_fields = ['uri', 'ip']
    readonly_fields = ['created', 'updated']
