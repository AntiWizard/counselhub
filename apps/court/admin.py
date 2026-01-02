from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from leaflet.admin import LeafletGeoAdmin

from apps.court.models import JudicialGeometry, JudicialAuthority
from apps.court.resources import JudicialGeometryResource
from utils import linkify


@admin.register(JudicialAuthority)
class JudicialAuthorityAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "archived")
    search_fields = ("name", "code")
    list_filter = ("archived",)


@admin.register(JudicialGeometry)
class JudicialGeometryAdmin(LeafletGeoAdmin, ImportExportModelAdmin):
    resource_class = JudicialGeometryResource

    list_display = ("name", linkify("judicial"), "code", "phone", "archived")
    search_fields = ("name", "code", "phone", "judicial__name", "judicial__code")
    list_filter = ("judicial", "archived")
    raw_id_fields = ("judicial",)

    fieldsets = (
        (
            _("basic_information"),
            {
                "fields": (
                    "judicial",
                    "name",
                    "phone",
                    "address",
                    "description",
                    "archived",
                )
            },
        ),
        (
            _("geometry"),
            {
                "fields": ("polygon",),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("judicial")
