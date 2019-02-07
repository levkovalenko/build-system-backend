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
        name = request.data.get("repository")
        if name is None:
            return HttpResponse('Not OK')
        name = name.get("name")
        if name is None:
            return HttpResponse('Not OK')
        tag = request.data.get("push_data")
        if tag is None:
            return HttpResponse('Not OK')
        tag = tag.get("tag")
        if tag is None:
            return HttpResponse('Not OK')

        if deploy.image_name == name and deploy.image_tag == tag:
            image_name = f"{deploy.owner.docker_username}/{name}:{tag}"
            if len(Container.objects.filter(deploy=deploy)) != 0:
                for container in Container.objects.filter(deploy=deploy):
                    con = client.containers.get(container.id)
                    con.kill()

            container = client.containers.run(image_name, '',
                                  ports=deploy.params.get("ports")
                                  )
            Container.objects.create(id=container.id, deploy=deploy)
        return HttpResponse('OK')
