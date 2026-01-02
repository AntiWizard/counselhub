import json
from import_export.widgets import Widget


class GeoJSONWidget(Widget):
    """
    - IMPORT: does NOT parse geometry (returns raw string)
    - EXPORT: outputs GeoJSON FeatureCollection
    """

    def clean(self, value, row=None, **kwargs):
        # IMPORTANT: do NOT convert here
        return value

    def render(self, value, obj=None, **kwargs):
        if not value:
            return ""

        try:
            geometry = json.loads(value.geojson)
        except Exception:
            return ""

        return json.dumps(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {},
                        "geometry": geometry,
                    }
                ],
            },
            ensure_ascii=False,
        )
