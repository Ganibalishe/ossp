import uuid

from django.db import models


class UUIDMixin(models.Model):
    id = models.UUIDField('id', default=uuid.uuid4, primary_key=True)

    class Meta:
        abstract = True


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class CreatedUpdatedMixin(CreatedAtMixin):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SortableMixin(models.Model):
    sort = models.IntegerField(default=0)

    class Meta:
        abstract = True


class IsPublishedMixin(models.Model):
    is_published = models.BooleanField('опубликован', default=True)

    class Meta:
        abstract = True
