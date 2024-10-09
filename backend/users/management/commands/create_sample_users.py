from django.core.management.base import BaseCommand
from users.models import User
from faker import Faker
from users.services.location import LocationService, LocationInfo

class Command(BaseCommand):
    help = 'Creates 50 sample users'

    def handle(self, *args, **kwargs):
        fake = Faker()
        location_service = LocationService()

        # Generate all zipcodes first
        zipcodes = [fake.zipcode() for _ in range(50)]

        # Get batch location info
        location_infos = location_service.get_batch_location_info(zipcodes)

        # Create users
        for zipcode in zipcodes:
            location_info = location_infos.get(zipcode, LocationInfo(city="Unknown", state="Unknown"))

            print (f"Creating user with zipcode {zipcode} and location {location_info.city}, {location_info.state}")

            User.objects.create(
                name=fake.name(),
                zipcode=zipcode,
                city=location_info.city,
                state=location_info.state
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 50 sample users'))