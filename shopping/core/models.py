from django.db import models


# Create your models here.
class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["_created"]  # order desc


class LogicalQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_deleted=True)

    def hard_delete(self):
        return super().delete()


class LogicalManager(models.Manager):
    def get_queryset(self):
        return LogicalQuerySet(self.model).filter(is_deleted=False, is_active=True)

    def archive(self):
        return LogicalQuerySet(self.model)

    def deleted(self):
        return LogicalQuerySet(self.model).filter(is_deleted=True)


class LogicalBaseModel(models.Model):
    is_active = models.BooleanField(default=True,verbose_name="فعال")
    is_deleted = models.BooleanField(default=False, verbose_name="حذف")

    objects = LogicalManager()

    class Meta:
        abstract = True
