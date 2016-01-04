from django.db import models
from django.contrib import admin

from .base import encrypt, decrypt


class Postfix(models.Model):
    server = models.OneToOneField('Server')
    hostname = models.CharField(max_length=50, default='')
    mysql_db = models.CharField(max_length=50, default='')
    mysql_user = models.CharField(max_length=50, default='')
    mysql_password = models.CharField(max_length=50, default='')
    mysql_salt = models.CharField(max_length=50, default='')

    class Meta:
        app_label = 'api'
        verbose_name = 'postfix'
        verbose_name_plural = 'postfix'
        ordering = ['server_id']

    def __str__(self):
        return self.hostname

    def get_password(self):
        return decrypt(self.mysql_password)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.mysql_password = encrypt(self.mysql_password)
        else:
            prev_password = Postfix.objects.get(id=self.id).mysql_password
            if prev_password != self.mysql_password:
                self.mysql_password = encrypt(self.mysql_password)
        super().save(*args, **kwargs)


class PostfixEmail(models.Model):
    postfix = models.ForeignKey(Postfix, related_name='emails')
    email = models.CharField(max_length=50, default='')
    password = models.CharField(max_length=50, default='')
    alias = models.CharField(max_length=50, default='', blank=True)

    class Meta:
        app_label = 'api'
        ordering = ['postfix_id']

    def __str__(self):
        return self.email

    def get_password(self):
        return decrypt(self.password)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = encrypt(self.password)
        else:
            prev_password = PostfixEmail.objects.get(id=self.id).password
            if prev_password != self.password:
                self.password = encrypt(self.password)
        super().save(*args, **kwargs)


class PostfixEmailInline(admin.TabularInline):
    model = PostfixEmail
    extra = 0


@admin.register(Postfix)
class PostfixAdmin(admin.ModelAdmin):
    inlines = (PostfixEmailInline,)
    list_display = (
        'server',
        'hostname',
        'mysql_db',
        'mysql_user',
        'mysql_salt'
    )


@admin.register(PostfixEmail)
class PostfixEmailAdmin(admin.ModelAdmin):
    list_display = ('postfix', 'email', 'alias')

    def get_model_perms(self, request):
        """Hide from index page"""
        return {}
