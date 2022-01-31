from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

INTERVAL_TIME = (
    ('15', '15 minute'),
    ('30', '30 minute'),
    ('45', '45 minute'),
)

# Create your models here.


class ExtendUser(models.Model):

    email = models.EmailField(
        blank=False, max_length=255, verbose_name="email")

# Create your models here.


class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    interval_time = models.CharField(max_length=100, choices=INTERVAL_TIME)

    class Meta:
        ordering = ['-start_date_time']

    def __str__(self):
        return self.user.username


class NonUser(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.email
