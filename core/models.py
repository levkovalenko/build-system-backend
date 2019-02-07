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


SOURCE_CHOICES = (
    ('d', 'docker'),
    ('s', 'docker_swarm'),
    ('g', 'github')
)


class Deploy(models.Model):
    url_prefix = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_name = models.CharField(max_length=256, blank=True, null=True)
    image_tag = models.CharField(max_length=256, blank=True, null=True)
    owner = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    source = models.CharField(max_length=1, blank=False, default='d', choices=SOURCE_CHOICES)
    params = JSONField(default=dict)

    def __str__(self):
        return f"{self.url_prefix} {self.image_name}:{self.image_tag}"


class Container(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    deploy = models.ForeignKey(Deploy,  null=False, blank=False, on_delete=models.CASCADE)
