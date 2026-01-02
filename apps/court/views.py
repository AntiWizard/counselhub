from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.court.models import JudicialAuthority, JudicialGeometry
from apps.court.serializers import (
    JudicialAuthoritySerializer,
    JudicialGeometrySerializer,
)


class ListJudicialApi(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = JudicialAuthority.objects.filter(archived=False).all()
    serializer_class = JudicialAuthoritySerializer


class ListMatchJudicialApi(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = JudicialGeometrySerializer

    def get_queryset(self):
        # ---- REQUIRED params ----
        judicial_ids = self.request.query_params.getlist("judicial_ids")
        lat = self.request.query_params.get("lat")
        lng = self.request.query_params.get("lng")

        if not judicial_ids or lat is None or lng is None:
            raise ValidationError(
                _("judicial_ids, lat and lng query parameters are required.")
            )

        try:
            lat = float(lat)
            lng = float(lng)
        except ValueError:
            raise ValidationError(
                _("judicial_ids, lat and lng query parameters are required.")
            )

        point = Point(lng, lat, srid=4326)

        return JudicialGeometry.objects.select_related("judicial").filter(
            judicial_id__in=judicial_ids,
            archived=False,
            judicial__archived=False,
            polygon__covers=point,
        )
