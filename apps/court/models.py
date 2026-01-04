import uuid

from django.db import models, transaction
from django.contrib.gis.db import models as gis_model
from django.db.models import Max
from django.utils.translation import gettext_lazy as _


class JudicialAuthority(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name=_("name"))
    code = models.PositiveIntegerField(
        unique=True, editable=False, verbose_name=_("code")
    )
    archived = models.BooleanField(default=False, verbose_name=_("archived"))

    def save(self, *args, **kwargs):
        if not self.code:
            with transaction.atomic():
                last_code = (
                    JudicialAuthority.objects.select_for_update()
                    .aggregate(max_code=Max("code"))
                    .get("max_code")
                )
                self.code = (last_code or 999) + 1  # starts at 1000
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.code}"

    class Meta:
        verbose_name = _("JudicialAuthority")
        verbose_name_plural = _("JudicialAuthorities")


class JudicialGeometry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    judicial = models.ForeignKey(
        JudicialAuthority,
        on_delete=models.CASCADE,
        related_name="geometries",
        verbose_name=_("judicial"),
    )
    name = models.CharField(max_length=511, verbose_name=_("name"))
    code = models.PositiveIntegerField(
        unique=True, editable=False, verbose_name=_("code")
    )
    address = models.CharField(
        max_length=511, null=True, blank=True, verbose_name=_("address")
    )
    phone = models.CharField(
        max_length=15, null=True, blank=True, verbose_name=_("phone")
    )
    description = models.TextField(null=True, blank=True, verbose_name=_("description"))
    archived = models.BooleanField(default=False, verbose_name=_("archived"))
    polygon = gis_model.PolygonField(verbose_name=_("geometry"))

    def save(self, *args, **kwargs):
        if not self.code:
            with transaction.atomic():
                last_code = (
                    JudicialGeometry.objects.select_for_update()
                    .aggregate(max_code=Max("code"))
                    .get("max_code")
                )
                self.code = (last_code or 99999) + 1  # starts at 100000
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("JudicialGeometry")
        verbose_name_plural = _("JudicialGeometries")
