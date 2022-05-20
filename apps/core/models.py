from django.db import models


class TimeStamp(models.Model):
    """ TimeStamp model. This model is used to store the creation and modification dates of the objects. """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
