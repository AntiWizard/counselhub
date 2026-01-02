import logging

import httpx
from django.conf import settings

from apps.general.exceptions import NeshanServiceCallError
from utils.singleton import Singleton
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger("custom")

NESHAN_ERROR_MAP = {
    400: _("neshan.invalid_argument"),
    470: _("neshan.coordinate_parse_error"),
    480: _("neshan.key_not_found"),
    481: _("neshan.limit_exceeded"),
    482: _("neshan.rate_exceeded"),
    483: _("neshan.api_key_type_error"),
    484: _("neshan.api_whitelist_error"),
    485: _("neshan.api_service_list_error"),
}


class NeshanService(metaclass=Singleton):
    BASE_URL = settings.NESHAN_API
    TOKEN = settings.NESHAN_TOKEN

    def get_search_data(self, term, lat, lng):
        return self._call_api_with_token(
            url=f"{self.BASE_URL}/v1/search",
            params={"term": term, "lat": lat, "lng": lng},
        )

    def get_search_detail_data(self, lat, lng):
        return self._call_api_with_token(
            url=f"{self.BASE_URL}/v5/reverse",
            params={"lat": lat, "lng": lng},
        )

    def _call_api_with_token(self, *, url, params=None, method="get", timeout=30):
        headers = {"Api-Key": self.TOKEN}

        try:
            response = httpx.request(
                method=method, url=url, headers=headers, params=params, timeout=timeout
            )
        except httpx.TimeoutException:
            raise NeshanServiceCallError()
        except httpx.HTTPError:
            raise NeshanServiceCallError()

        if response.status_code == 200:
            return response.json()

        # 🔹 Known user-related errors
        if response.status_code in NESHAN_ERROR_MAP:
            print(NESHAN_ERROR_MAP[response.status_code])
            raise NeshanServiceCallError()
        raise NeshanServiceCallError()
