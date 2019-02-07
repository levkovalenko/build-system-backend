from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField, JSONField
import uuid


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


class User(AbstractUser):
    docker_username = models.CharField(max_length=256, blank=True, null=True)
    docker_password = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return f"{self.username, self.email}"


class Params(models.Model):
    in_port = models.IntegerField( blank=True, null=True)
    out_port = models.IntegerField( blank=True, null=True)
    path_inside = models.CharField(max_length=256, blank=True, null=True)
    path_outside = models.CharField(max_length=256, blank=True, null=True)
    mode = models.CharField(max_length=256, blank=True, null=True)

    def get_ports(self):
        return {f'{self.in_port}/tcp': self.out_port}

    def get_paths(self):
        return {self.path_inside: {'bind': self.path_outside, 'mode': self.mode}}


SOURCE_CHOICES = (
    ('d', 'docker'),
    ('s', 'docker_swarm'),
    ('g', 'github')
)


class Deploy(models.Model):
    url_prefix = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    source = models.CharField(max_length=1, blank=False, default='d', choices=SOURCE_CHOICES)
    params = models.OneToOneField(Params, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.url_prefix}"


class Image(models.Model):
    image_name = models.CharField(max_length=256, blank=True, null=True)
    image_tag = models.CharField(max_length=256, blank=True, null=True)
    deploy = models.OneToOneField(Deploy,  null=True, on_delete=models.CASCADE)

    def get_name(self):
        return f'{self.deploy.owner.docker_username}/{self.image_name}:{self.image_tag}'


class Container(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    image = models.OneToOneField(Image,  null=True, on_delete=models.SET_NULL)


