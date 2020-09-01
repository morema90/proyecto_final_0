from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import uuid


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class create_event(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_name = models.CharField(max_length=100)
    category_events = (('CONFERENCE', 'Conferencia'), ('SEMINAR', 'Seminario'), ('CONGRESS', 'Congreso'), ('COURSE', 'Curso'))
    event_category = models.CharField(max_length=10, choices=category_events, null=False, blank=False)
    event_place = models.CharField(max_length=100)
    event_address = models.CharField(max_length=100)
    event_initial_date = models.DateTimeField()
    event_final_date = models.DateTimeField()
    types_events = (('PRESENCIAL', 'Presencial'), ('VIRTUAL', 'Virtual'))
    event_type = models.CharField(max_length=10, choices=types_events, null=False, blank=False)
    event_creation_date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField("Imagen", upload_to="thumbnails", default="thumbnails/default.png")

    class Meta:
        ordering = ['-event_creation_date']

    def __str__(self):
        return self.event_name