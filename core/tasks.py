from celery.signals import worker_ready
from django.conf import settings
from django.db.models import Q
from core.models import *
import celery
import docker
from backend.celery import app


def task_prerun(fn, prerun):
    def wrapped(*args, **kwargs):
        prerun(*args, **kwargs)
        return fn(*args, **kwargs)

    return wrapped


class MetaBaseTask(type):
    def __init__(cls, name, bases, attrs):
        cls.name = name
        cls.run = task_prerun(cls.run, getattr(cls, 'on_prerun'))
        super().__init__(cls)


class BaseTask(celery.Task, metaclass=MetaBaseTask):
    serializer = settings.CELERY_TASK_SERIALIZER
    max_retries = 3
    ignore_result = True
    default_retry_delay = 5

    def __init__(self):
        self.client = docker.from_env()

    def on_prerun(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        return super().run(*args, **kwargs)

    def on_success(self, retval, task_id, args, kwargs):
        pass


class DockerDeploy(BaseTask):
    def run(self, deploy_uid):
        print(deploy_uid)
        deploy = Deploy.objects.get(url_prefix=deploy_uid)
        owner = deploy.owner
        params = deploy.params
        image_model = deploy.image
        image_name = image_model.get_name()
        try:
            image = self.client.images.get(image_name)
        except docker.errors.ImageNotFound:
            image = None
        if get_or_none(Container, image=image_model) is not None:
            container_model = get_or_none(Container, image=image_model)
            container = self.client.containers.get(container_model.id)
            container.kill()
            container.remove(force=True)
            container_model.delete()
        if image is not None:
            self.client.images.remove(image=image_name, force=True)
        container = self.client.containers.run(
            image_model.get_name(),
            ports=params.get_ports(),
            volumes=params.get_paths(),
            detach=True,
        )
        Container.objects.create(id=container.id, image=image_model)


app.tasks.register(DockerDeploy())


@worker_ready.connect()
def at_start(sender, **k):
    pass
