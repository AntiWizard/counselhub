from rest_framework import serializers

from apps.court.models import JudicialAuthority, JudicialGeometry


class JudicialAuthoritySerializer(serializers.ModelSerializer):
    """
    Serializer for JudicialAuthority model
    """

    class Meta:
        model = JudicialAuthority
        fields = ["id", "name", "code"]


class JudicialGeometrySerializer(serializers.ModelSerializer):
    """
    Serializer for JudicialGeometry model
    """

    polygon = serializers.SerializerMethodField()
    judicial = JudicialAuthoritySerializer(read_only=True)

    class Meta:
        model = JudicialGeometry
        fields = [
            "id",
            "name",
            "address",
            "phone",
            "description",
            "polygon",
            "judicial",
        ]

    def get_polygon(self, obj):
        polygon = getattr(obj, "polygon", None)
        return str(polygon) if polygon else None
