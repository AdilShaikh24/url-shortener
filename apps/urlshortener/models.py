# Standard Library Imports
import random
import string

# Third Party Imports
from django.db import models

# Local Imports
from apps.common.mixins import AuditMixin


# Create your models here.
class ShortenedURL(AuditMixin):
    long_url = models.URLField()
    short_code = models.CharField(max_length=6, unique=True)

    @staticmethod
    def generate_unique_short_code():
        length = 6
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choices(chars, k=length))
