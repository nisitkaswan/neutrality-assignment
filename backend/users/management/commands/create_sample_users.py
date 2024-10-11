from django.core.management.base import BaseCommand
from users.models import User
from faker import Faker
from users.services.location import LocationService, LocationInfo
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Creates 50 sample users with location information'

    def handle(self, *args, **kwargs):

        User.objects.all().delete()

        fake = Faker()
        location_service = LocationService()

        # Generate all zipcodes first
        zipcodes = [fake.zipcode() for _ in range(50)]

        try:
            # Get batch location info
            location_infos = location_service.get_batch_location_info(zipcodes)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error fetching location info: {e}'))
            logger.error(f'Error fetching location info: {e}', exc_info=True)
            return

        # Create users
        for zipcode in zipcodes:
            location_info = location_infos.get(zipcode, LocationInfo(city="Unknown", state="Unknown"))

            self.stdout.write(f"Creating user with zipcode {zipcode} and location {location_info.city}, {location_info.state}")

            try:
                User.objects.create(
                    name=fake.name(),
                    zipcode=zipcode,
                    city=location_info.city,
                    state=location_info.state
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error creating user with zipcode {zipcode}: {e}'))
                logger.error(f'Error creating user with zipcode {zipcode}: {e}', exc_info=True)

        self.stdout.write(self.style.SUCCESS('Successfully created sample users'))