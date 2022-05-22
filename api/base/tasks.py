from celery import shared_task
from celery.utils.log import get_task_logger

from base.models import Drone, DroneStatusLog

logger = get_task_logger(__name__)

@shared_task
def check_drone_battery_task():
    for drone in Drone.objects.all():
        message = 'Drone {} have a battery capacity of {}'.format(drone.serial_number, drone.battery_capacity)
        if drone.battery_capacity >= 25:
            logger.info(message)
        else:
            logger.warning(message)

        DroneStatusLog.objects.create(
            drone_rel=drone,
            current_battery=drone.battery_capacity
        )