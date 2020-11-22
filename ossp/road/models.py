from django.db import models

# Create your models here.
from core.models import UUIDMixin


class Road(UUIDMixin):
    name = models.CharField('название', max_length=100)

    class Meta:
        verbose_name = 'трасса'
        verbose_name_plural = 'трассы'

    def __str__(self):
        return self.name


class Section(UUIDMixin):
    name = models.CharField('название секции', max_length=150)
    road = models.ForeignKey(Road, verbose_name='трасса', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'секция'
        verbose_name_plural = 'секции'

    def __str__(self):
        return f'{self.road} - {self.name}'


class Point(UUIDMixin):
    name = models.CharField('название точки', max_length=150)
    section = models.ForeignKey(Section, verbose_name='секция', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'точка'
        verbose_name_plural = 'точки'

    def __str__(self):
        return self.name

    def get_name_with_section(self):
        return f'{self.section} - {self.name}'
