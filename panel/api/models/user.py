from django.contrib import admin
from django.db import models


from .base import encrypt, decrypt


class User(models.Model):
    ERROR_MESSAGE_01 = 'Project DB may have only one User.'

    DB = 'db'
    SERVER = 'server'
    TYPE_CHOICES = ((DB, 'DB'), (SERVER, 'Server'))

    server = models.ForeignKey(
        'Server', null=True, blank=True, default=None,
        verbose_name='server (VPS)')
    db = models.ForeignKey(
        'Db', null=True, blank=True, default=None, related_name='users',
        verbose_name='database')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'api'
        ordering = ('-server', 'type', 'name')

    def __str__(self):
        return self.name

    def get_password(self):
        return decrypt(self.password)

    def check_for_single(self):
        """Checking for project db that may have only one user"""
        if self.type == User.SERVER:
            return True

        Db = self.db.__class__
        if self.db.type == Db.PROJECT:
            count = User.objects.filter(db_id=self.db_id).count()
            if count > 0:
                return False
        return True

    def save(self, *args, **kwargs):
        # crypt password
        if not self.pk:
            self.password = encrypt(self.password)
        else:
            prev_password = User.objects.get(id=self.id).password
            if prev_password != self.password:
                self.password = encrypt(self.password)

        if not self.pk:
            if self.check_for_single() is False:
                raise Exception(self.ERROR_MESSAGE_01)
        super().save(*args, **kwargs)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'server', 'db')
    list_filter = ('type',)
    search_fields = ('name',)

    def add_view(self, request, extra_context=None):
        title = 'Add either "Server" or "Database" user.'
        extra_context = extra_context or {}
        extra_context['title'] = title

        self.fields = ('server', 'db', 'name', 'password', 'is_active')
        self.readonly_fields = ()
        return super().add_view(request, extra_context=extra_context)

    def change_view(self, request, object_id):
        self.readonly_fields = ('server', 'db', 'name')

        obj = User.objects.get(id=object_id)
        fields = ('name', 'password')
        if obj.type == User.SERVER:
            self.fields = ('server',) + fields
        elif obj.type == User.DB:
            self.fields = ('db',) + fields
        return super().change_view(request, object_id)

    def save_model(self, request, obj, form, change):
        """Automatically determines the type of user"""
        if obj.server:
            obj.type = User.SERVER

        if obj.db:
            obj.type = User.DB
            obj.server = None

        obj.save()


class UserInline(admin.TabularInline):
    model = User
    extra = 0
