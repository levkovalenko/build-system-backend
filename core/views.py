from django.http import HttpResponse
from rest_framework import viewsets
from core.models import *
from core.tasks import DockerDeploy


class WebHookViewSet(viewsets.ViewSet):
    def get(self, request, prefix):
        deploy = get_or_none(Deploy, url_prefix=prefix)
        print(deploy)
        if deploy is None:
            return HttpResponse('Not OK')
        DockerDeploy().apply_async(args=(prefix,))
        return HttpResponse('OK')
