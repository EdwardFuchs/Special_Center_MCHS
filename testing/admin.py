from attr.filters import exclude
from django.contrib import admin
from .models import TestModel, Profile, FileModel, PunishmentModel
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


admin.site.register(TestModel)


class UserInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "профиль"


# Определяем новый класс настроек для модели User
class UserAdminNew(UserAdmin):
    inlines = (UserInline,)


class TestImageInline(admin.StackedInline):
    model = FileModel
    extra = 0
    can_delete = True
    verbose_name_plural = "файлы"


class TestProfileInline(admin.StackedInline):
    model = PunishmentModel
    extra = 0
    can_delete = True
    # fields = []
    verbose_name_plural = "привлеченные пользователи"


class TestAdmin(admin.ModelAdmin):
    inlines = (TestImageInline, TestProfileInline)
    readonly_fields = ['user']
    # raw_id_fields = ['user']


# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, UserAdminNew)

admin.site.unregister(TestModel)
admin.site.register(TestModel, TestAdmin)

