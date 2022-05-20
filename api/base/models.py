from django.db import models
from django.utils.translation import ugettext_lazy as _


class CommonInfo(models.Model):
    """
    Base abstract model to data shared for all models
    """

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        abstract = True


class Drone(CommonInfo):
    """
    Store the data of the drones
    """

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

    def __str__(self) -> str:
        return self.serial_number


class Flight(CommonInfo):
    """
    A flight for a drone represent the process of the drone to transport several load
    on a time interval.
    This model storage a history of flights for each drone and the state of load for the current flight
    * A drone can only had one flight with the was_delivered on False at the same time.
    * That means that a drone on IDLE state do not have any flight yet or all the flights had false on was_delivered field
    * A drone when enters on DELIVERING state need to asign a datetime to start_datetime
    * A drone when enter to the state IDLE from RETURNING need to asign a datetime to arrive_datetime
    """

    drone_rel = models.ForeignKey(
        Drone,
        verbose_name=_('Drone'),
        on_delete=models.CASCADE,
        null=False
    )

    start_datetime = models.DateTimeField(
        null=True,
        verbose_name=_("Start datetime")
    )
    arrive_datetime = models.DateTimeField(
        null=True,
        verbose_name=_('Arrived')
    )

    was_delivered = models.BooleanField(
        verbose_name=_('Was delivered?'),
        default=False
    )

    def __str__(self) -> str:
        return "Flight {}-{}".format(self.drone_rel.serial_number, self.created)


class Medication(CommonInfo):
    """
    Store medication data
    """

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

    def __str__(self) -> str:
        return self.name


class Load(CommonInfo):
    flight_rel = models.ForeignKey(
        Flight,
        verbose_name=_('Flight'),
        on_delete=models.CASCADE,
        null=False,
    )

    medication_rel = models.ForeignKey(
        Medication,
        verbose_name=_('Medication'),
        on_delete=models.PROTECT,
        null=False,
    )

    quantity = models.IntegerField(
        verbose_name=_('Quantity'),
        default=1,
        null=False,
        blank=False,
    )

    class Meta:
        unique_together = [['flight_rel', 'medication_rel']]

    def __str__(self) -> str:
        return "{}-{}".format(self.flight_rel, self.medication_rel)