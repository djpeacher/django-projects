# django-user-solo

Proof of concept `UserSingletonModel` that creates an singleton instance for each user.

Inspired by [django-solo](https://github.com/lazybird/django-solo) ❤️

```python
from user_solo.models import UserSingletonModel

class Preference(UserSingletonModel):
    flag = models.BooleanField(default=True)

# All users will have .preference
user = User.objects.get(...)
user.preference # get_or_create
```

### TODO

- Settings
- Caching
- Signals (create when user created)
