from django.db import models


class BaseModel(models.Model):
    """Абстрактная базовая модель сервиса."""

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id}"
