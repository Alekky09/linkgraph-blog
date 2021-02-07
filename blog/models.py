from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Writer(AbstractUser):
    is_editor = models.BooleanField(default=False)
    name = models.CharField(max_length=24)


class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)
    content = models.TextField()
    status = models.BooleanField(null=True)
    written_by = models.ForeignKey(
                                    Writer,
                                    on_delete=models.CASCADE,
                                    related_name="written"
                                )
    edited_by = models.ManyToManyField(
                                    Writer,
                                    blank=True,
                                    related_name="edited"
                                )
    reviewed_by = models.ForeignKey(
                                    Writer,
                                    on_delete=models.SET_DEFAULT,
                                    default=None,
                                    null=True,
                                    blank=True,
                                    related_name="reviewed"
                                )
