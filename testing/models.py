from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import User
from time import time as current_time
from .choices import SCORE, RANK, PUNISHMENT
from uuid import uuid4


def user_directory_path(instance, filename):
    return f"{current_time()}_{uuid4().int}/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    middleName = models.CharField("Отчество", max_length=30)
    rank = models.CharField(
        "Должность",
        max_length=2,
        choices=RANK,
        default="u",
    )

    def __str__(self):
        rank = None
        for el in RANK:
            if el[0] == self.rank:
                rank = el[1]
        return f"{self.user.last_name} {self.user.first_name} {self.middleName} (Должность - {rank})"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


# class Employee(models.Model):
#     fio = models.CharField("ФИО", max_length=150)
#     rank = models.CharField(
#         "Должность",
#         max_length=2,
#         choices=RANK,
#         default="u",
#     )
#


class TestModel(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE , null=True, blank=True, verbose_name="Отправитель")
    name = models.CharField("Название проверки", max_length=150)  # название проверки
    score = models.IntegerField("Оценка", choices=SCORE)  # Оценка
    text = models.CharField("Основные недостатки", max_length=1500)  # основные недостатки
    elimination_plan = models.FileField("План исправления недостатков", upload_to=user_directory_path)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Проверка"
        verbose_name_plural = "Проверки"
        ordering = ["id"]


class FileModel(models.Model):
    test = models.ForeignKey(TestModel, on_delete=models.CASCADE)
    file = models.FileField("Файл", upload_to=user_directory_path)

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = "Файлы"
        verbose_name_plural = "Файлы"


class PunishmentModel(models.Model):
    test = models.ForeignKey(TestModel, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Сотрудник")
    punishment = models.CharField(
        "Наказание",
        max_length=8,
        choices=PUNISHMENT,
        default="type0",
    )

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "Наказания"
        verbose_name_plural = "Наказания"

