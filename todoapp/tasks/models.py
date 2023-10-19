from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=150)
    complete = models.BooleanField(default=False)
    created = models.TimeField(auto_now_add=True)
    date = models.DateField(default=timezone.localdate)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']
