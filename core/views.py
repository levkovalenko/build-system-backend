from django.http import HttpResponse
from rest_framework import viewsets
from core.models import *


class WebHookViewSet(viewsets.ViewSet):
    def get(self, request, prefix):
        print(prefix)
        deploy = get_or_none(Deploy, url_prefix=prefix)
        if deploy is None:
            return HttpResponse('OK')
        print(deploy.url_prefix)
        return HttpResponse('OK')
