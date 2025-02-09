# Third Party Imports
from django.db.models import DateTimeField, Model


class AuditMixin(Model):
    """Adds auditing metadata to the model"""

    created_at = DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = DateTimeField(auto_now=True, editable=False, null=True)

    class Meta:
        abstract = True
