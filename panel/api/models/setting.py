from django.db import models
from django.contrib import admin

TYPES = [(1, 'str'), (2, 'int')]


class Setting(models.Model):
    code = models.CharField(max_length=50)
    value = models.CharField(max_length=255, default='', blank=True)
    info = models.CharField(max_length=255, default='', blank=True)
    type = models.SmallIntegerField(choices=TYPES, default=1, blank=True)

    class Meta:
        app_label = 'api'

        def __str__(self):
            return self.code


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    forbid_deleting_codes = ['001', '002', '003', '004']

    actions = None
    fields = ('code', 'type', 'value', 'info')
    list_display = ('code', 'value', 'info', 'type')
    list_editable = ('type',)

    def add_view(self, request, extra_context=None):
        self.readonly_fields = ()
        return super().add_view(request, extra_context=extra_context)

    def change_view(self, request, object_id):
        self.readonly_fields = ('code', 'info', 'type')
        return super().change_view(request, object_id)

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return False

        if obj.code in self.forbid_deleting_codes:
            return False
        return super().has_delete_permission(request, obj)
