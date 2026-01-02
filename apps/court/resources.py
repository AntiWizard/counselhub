from functools import cached_property

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from import_export import resources, fields

from apps.court.models import JudicialAuthority, JudicialGeometry
from apps.court.uitils import parse_polygon
from apps.court.widgets import GeoJSONWidget

MAX_IMPORT_ROWS = 10_000


class JudicialGeometryResource(resources.ModelResource):
    judicial_code = fields.Field(column_name="judicial_code")
    polygon = fields.Field(
        column_name="polygon", attribute="polygon", widget=GeoJSONWidget()
    )

    class Meta:
        model = JudicialGeometry
        import_id_fields = ("code",)
        skip_unchanged = False
        report_skipped = True
        fields = (
            "judicial_code",
            "code",
            "name",
            "address",
            "description",
            "phone",
            "polygon",
        )

    def before_import(self, dataset, **kwargs):
        row_count = len(dataset)
        if row_count > MAX_IMPORT_ROWS:
            raise ValidationError(
                _(
                    "The uploaded file contains %(count)d rows. "
                    "The maximum allowed rows for import is %(max)d."
                )
                % {"count": row_count, "max": MAX_IMPORT_ROWS}
            )

    def get_queryset(self):
        return super().get_queryset().select_related("judicial")

    @cached_property
    def judicial_map(self):
        return {ja.code: ja.id for ja in JudicialAuthority.objects.only("id", "code")}

    def before_import_row(self, row, **kwargs):
        judicial_code = row.get("judicial_code")
        if not judicial_code:
            raise ValidationError(_("judicial_code_is_required"))

        if judicial_code not in self.judicial_map:
            raise ValidationError(
                _("judicial_authority_code_not_found_with_code")
                % {"code": judicial_code}
            )

        code = row.get("code")
        if code:
            row["code"] = str(int(float(code)))

    def before_save_instance(self, instance, row, **kwargs):
        instance.judicial_id = self.judicial_map[row["judicial_code"]]

        polygon_value = row.get("polygon")
        if polygon_value:
            instance.polygon = parse_polygon(polygon_value)

    def dehydrate_judicial_code(self, obj):
        return obj.judicial.code if obj.judicial_id else ""

    def get_import_fields(self):
        return [
            field for field in self.fields.values() if field.column_name != "polygon"
        ]
