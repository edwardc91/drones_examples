from django.db import models
from django.db.models import Sum, F
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator


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
        default=500,
        validators=[
            MaxValueValidator(
                limit_value=500,
                message=_('Weight limit cannot be greater than 500.'),
            ),
            MinValueValidator(
                limit_value=1,
                message=_('Weight limit cannot be less than 1.'),
            )
        ]
    )

    battery_capacity = models.FloatField(
        blank=False,
        null=False,
        verbose_name=_('Weight limit'),
        default=100,
        validators=[
            MaxValueValidator(
                limit_value=100,
                message=_('Battery capacity cannot be greater than 100.'),
            ),
            MinValueValidator(
                limit_value=0,
                message=_('Battery capacity cannot be less than 0.'),
            )
        ]
    )

    state = models.CharField(
        max_length=15,
        choices=STATE_CHOICES,
        default=STATE_CHOICES[0][0],
        verbose_name=_('State'),
        blank=False,
        null=False,
    )

    def is_ready_to_flight(self):
        state = self.state
        battery = self.battery_capacity
        return (state == 'IDLE' and battery >= 25 ) or state == 'LOADING' or state == 'LOADED'


    def get_load_weight(self):
        current_flight = self.flights_rel.filter(was_delivered=False)
        if current_flight.exists():
            return current_flight[0].loads_rel.annotate(quantity_x_weight=F('medication_rel__weight') * F('quantity')).aggregate(
                total_load=Sum(
                    'quantity_x_weight'
                ))['total_load']  
        else:
            return 0

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(weight_limit__lte=500), name='weight_limit_lte_500'),
            models.CheckConstraint(check=models.Q(weight_limit__gte=0), name='weight_limit_gte_0'),
            models.CheckConstraint(check=models.Q(battery_capacity__lte=100), name='battery_capacity_lte_100'),
            models.CheckConstraint(check=models.Q(battery_capacity__gte=0), name='battery_capacity_gte_0'),
        ]

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
        null=False,
        related_name='flights_rel',
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
        default=1,
        validators=[
            MaxValueValidator(
                limit_value=500,
                message=_('Weight cannot be greater than 500.'),
            ),
            MinValueValidator(
                limit_value=1,
                message=_('Weight cannot be less than 1.'),
            )
        ]
    )

    code = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name=_('Code'),
        unique=True,
        validators=[
            RegexValidator(
                regex='^([A-Z0-9]|-|_)+$',
                message=_('Invalid medication code.'),
            ),
        ],
    )

    image = models.ImageField(
        verbose_name=_('Image'),
        null=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(weight__lte=500), name='weight_lte_500'),
            models.CheckConstraint(check=models.Q(weight__gt=0), name='weight_gt_0'),
        ]


class Load(CommonInfo):
    flight_rel = models.ForeignKey(
        Flight,
        verbose_name=_('Flight'),
        on_delete=models.CASCADE,
        null=False,
        related_name='loads_rel',
    )

    medication_rel = models.ForeignKey(
        Medication,
        verbose_name=_('Medication'),
        on_delete=models.PROTECT,
        null=False,
        related_name='loads_rel',
    )

    quantity = models.IntegerField(
        verbose_name=_('Quantity'),
        default=1,
        null=False,
        blank=False,
    )

    def get_weight(self):
        return self.medication_rel.weight * self.quantity

    class Meta:
        unique_together = [['flight_rel', 'medication_rel']]

    def __str__(self) -> str:
        return "{}-{}".format(self.flight_rel, self.medication_rel)


class DroneStatusLog(CommonInfo):
    """
    Historic status of the drones
    """

    drone_rel = models.ForeignKey(
        Drone,
        related_name='status_log_rel',
        on_delete=models.CASCADE,
        null=False,
        verbose_name=_('Drone')
    )

    current_battery = models.FloatField(
        verbose_name=_('Current battery'),
        null=True
    )

    def drone_name(self):
        return self.drone_rel.serial_number

    drone_name.short_description = _('Drone serial number')
    
    def __str__(self) -> str:
        return "{} {}".format(self.drone_rel.serial_number, self.created)

    class Meta:
        verbose_name = _("Drone's status log")