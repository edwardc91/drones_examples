from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class CommonInfo(models.Model):
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        abstract = True


class Drone(CommonInfo):
    MODEL_CHOICES = [
        ('Lightweight', _('Lightweight')),
        ('Middleweight', _('Middleweight')),
        ('Cruiserweight', _('Cruiserweight')),
        ('Heavyweight', _('Heavyweight')),
    ]

    STATE_CHOICES = [
        ('IDLE', 'Idle'),
        ('LOADING', 'Loading'),
        ('LOADED', 'Loaded'),
        ('DELIVERING', 'Delivering'),
        ('DELIVERED', 'Delivered'),
        ('RETURNING', 'Returning'),
    ]

    serial_number = models.CharField(
        max_length=100, 
        verbose_name=_('Serial number'), 
        unique=True, 
        null=False,
        blank=False
    )

    model = models.CharField(
        max_length=20,
        choices=MODEL_CHOICES,
        default=MODEL_CHOICES[0][0],
        verbose_name=_('Model'),
        blank=False,
        null=False,
    )

    weight_limit = models.FloatField(
        blank=False,
        null=False,
        verbose_name=_('Weight limit'),
        default=500
    )

    battery_capacity = models.FloatField(
        blank=False,
        null=False,
        verbose_name=_('Weight limit'),
        default=100
    )

    state = models.CharField(
        max_length=15,
        choices=STATE_CHOICES,
        default=STATE_CHOICES[0][0],
        verbose_name=_('State'),
        blank=False,
        null=False,
    )


class Medication(CommonInfo):
    name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        verbose_name=_('Name'),
        max_length=200,
    )

    weight = models.FloatField(
        blank=False,
        null=False,
        verbose_name=_('Weight'),
        default=1
    )

    code = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name=_('Code'),
        unique=True
    )

    image = models.ImageField(
        verbose_name=_('Image'),
        null=True,
    )
