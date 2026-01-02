import json
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def parse_polygon(value):
    if not value:
        return None

    value = value.strip().lstrip("\ufeff")

    try:
        data = json.loads(value)
    except Exception:
        raise ValidationError(_("invalid_polygon_format"))

    # FeatureCollection
    if data.get("type") == "FeatureCollection":
        features = data.get("features") or []
        if not features:
            raise ValidationError(_("empty_feature_collection"))
        geometry = features[0].get("geometry")

    elif data.get("type") == "Feature":
        geometry = data.get("geometry")

    else:
        geometry = data

    if not geometry:
        raise ValidationError(_("invalid_polygon_format"))

    if geometry.get("type") == "Polygon":
        coords = geometry.get("coordinates")
        if coords and isinstance(coords[0][0], (int, float)):
            geometry["coordinates"] = [coords]

    try:
        return GEOSGeometry(json.dumps(geometry), srid=4326)
    except Exception:
        raise ValidationError(_("invalid_polygon_geometry"))
