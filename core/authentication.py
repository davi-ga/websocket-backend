from rest_framework.authentication import SessionAuthentication
from drf_spectacular.extensions import OpenApiAuthenticationExtension


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass


class CsrfExemptSessionAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "core.authentication.CsrfExemptSessionAuthentication"
    name = "sessionAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "cookie",
            "name": "sessionid",
        }
