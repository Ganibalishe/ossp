from django.contrib.auth.models import User
from django.db import models

from core.models import CreatedAtMixin, UUIDMixin
from road.models import Road, Section, Point


class Commissioner(CreatedAtMixin, UUIDMixin):
    user = models.OneToOneField(User, verbose_name='user', on_delete=models.CASCADE)
    first_name = models.CharField('имя', max_length=75)
    surname = models.CharField('фамилия', max_length=75)
    patronymic = models.CharField('отчество', max_length=75)
    road = models.ForeignKey(Road, verbose_name='трасса', on_delete=models.SET_NULL, blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='секция', on_delete=models.SET_NULL, blank=True, null=True)
    point = models.ForeignKey(Point, verbose_name='точка', on_delete=models.SET_NULL, blank=True, null=True)
    password = models.CharField('пароль', max_length=12, blank=True, null=True)
    phone = models.CharField('телефон', max_length=11, unique=True)

    class Meta:
        verbose_name = 'аварийный комиссар'
        verbose_name_plural = 'аварийные комиссары'

    def __str__(self):
        return f'{self.surname} {self.first_name} {self.patronymic}'

    def get_full_name(self):
        return f'{self.surname} {self.first_name} {self.patronymic}'


class Dispatcher(CreatedAtMixin, UUIDMixin):
    user = models.OneToOneField(User, verbose_name='user', on_delete=models.CASCADE)
    first_name = models.CharField('имя', max_length=75)
    surname = models.CharField('фамилия', max_length=75)
    patronymic = models.CharField('отчество', max_length=75)
    road = models.ForeignKey(Road, verbose_name='трасса', on_delete=models.SET_NULL, blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='секция', on_delete=models.SET_NULL, blank=True, null=True)
    password = models.CharField('пароль', max_length=12, blank=True, null=True)
    phone = models.CharField('телефон', max_length=11, unique=True)

    class Meta:
        verbose_name = 'диспетчер'
        verbose_name_plural = 'диспетчеры'

    def __str__(self):
        return f'{self.surname} {self.first_name} {self.patronymic}'

    def get_full_name(self):
        return f'{self.surname} {self.first_name} {self.patronymic}'
