# django-user-solo

Proof of concept `AutoOneToOneField` that creates an singleton instance for each user.

Inspired by [django-solo](https://github.com/lazybird/django-solo) ❤️

```python
from user_solo.models import AutoOneToOneField

class Preference(models.Model):
    user = AutoOneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flag = models.BooleanField(default=True)

# All users will have .preference
user = User.objects.get(...)
user.preference # get_or_create
```
