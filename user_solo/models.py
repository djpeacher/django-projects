from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor
from django.db.models.fields.related import OneToOneField

class UserSingletonDescriptor(ReverseOneToOneDescriptor):
    def __get__(self, user, cls=None):
        try:
            return super().__get__(user, cls)
        except ObjectDoesNotExist:
            return self.related.related_model.objects.create(user=user)

class UserSingletonField(OneToOneField):
    related_accessor_class = UserSingletonDescriptor

class UserSingletonModel(models.Model):
    user = UserSingletonField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True