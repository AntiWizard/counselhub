from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.general.exceptions import InvalidInputFormatError
from apps.general.services.neshan import NeshanService


class GetSearchNeshanApi(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            lat = float(request.query_params.get("lat", 35.7026))
            lng = float(request.query_params.get("lng", 51.3368))
        except ValueError:
            raise InvalidInputFormatError()

        term = request.query_params.get("term")
        if not term:
            raise InvalidInputFormatError()

        data = NeshanService().get_search_data(term, lat, lng)
        return Response(data, status=status.HTTP_200_OK)
