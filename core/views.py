from django.http import HttpResponse
from rest_framework import viewsets
from core.models import *
import docker

client = docker.from_env()


class WebHookViewSet(viewsets.ViewSet):
    def get(self, request, prefix):
        deploy = get_or_none(Deploy, url_prefix=prefix)
        if deploy is None:
            return HttpResponse('Not OK')


        return HttpResponse('OK')
