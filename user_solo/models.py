from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor
from django.db.models.fields.related import OneToOneField

class AutoReverseOneToOneDescriptor(ReverseOneToOneDescriptor):
    def __get__(self, user, cls=None):
        try:
            return super().__get__(user, cls)
        except ObjectDoesNotExist:
            return self.related.related_model.objects.create(user=user)

class AutoOneToOneField(OneToOneField):
    related_accessor_class = AutoReverseOneToOneDescriptor