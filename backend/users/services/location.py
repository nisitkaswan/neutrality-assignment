from typing import Dict, List, Union, Optional

from django.conf import settings
from pydantic import BaseModel, Field, RootModel
from openai import OpenAI
import instructor


class LocationInfo(BaseModel):
    """Represents location information for a US zipcode."""
    city: str = Field(description="The name of the city.")
    state: str = Field(description="The two-letter state code.")

    def __str__(self):
        return f"{self.city}, {self.state}"


class SingleLocationInfo(BaseModel):
    """Represents location information for a single US zipcode."""
    zipcode: str = Field(description="The 5-digit US zipcode.")
    city: str = Field(description="The name of the city.")
    state: str = Field(description="The two-letter state code.")

    def to_location_info(self) -> LocationInfo:
        return LocationInfo(city=self.city, state=self.state)


class BatchLocationInfo(BaseModel):
    """Represents location information for multiple US zipcodes."""
    locations: Dict[str, LocationInfo] = Field(
        description="A dictionary mapping zipcodes to their location information.",
    )


class BatchLocationList(RootModel):
    """Represents a list of SingleLocationInfo objects."""
    root: List[SingleLocationInfo]


class LocationService:
    def __init__(self):
        self.client = instructor.from_openai(OpenAI(api_key=settings.OPENAI_API_KEY))
        print("LocationService initialized")

    def get_single_location_info(self, zipcode: str) -> LocationInfo:
        """Get the city and state for a single US zipcode."""
        print(f"Getting location info for zipcode: {zipcode}")
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                response_model=SingleLocationInfo,
                messages=[
                    {"role": "system",
                     "content": "You are a helpful assistant that provides accurate US location information."},
                    {"role": "user", "content": f"Provide the city and state for the US zipcode: {zipcode}."}
                ],
                max_retries=2
            )

            print(f"Raw API response: {response}")
            return response.to_location_info()

        except Exception as e:
            print(f"ERROR: Error calling OpenAI API for zipcode {zipcode}: {e}")
            import traceback
            print(traceback.format_exc())
            return LocationInfo(city="Unknown", state="Unknown")

    def get_location_info(self, zipcode: str) -> LocationInfo:
        """Get the city and state for a given US zipcode."""
        return self.get_single_location_info(zipcode)

    def get_batch_location_info(self, zipcodes: List[str]) -> Dict[str, LocationInfo]:
        """Get the city and state for a batch of US zipcodes."""
        print(f"Getting batch location info for {len(zipcodes)} zipcodes")
        try:
            zipcodes_str = ", ".join(zipcodes)
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                response_model=Union[BatchLocationInfo, BatchLocationList],
                messages=[
                    {"role": "system",
                     "content": "You are a helpful assistant that provides accurate US location information."},
                    {"role": "user",
                     "content": f"For each of the following US zipcodes, provide the city and state: {zipcodes_str}. "
                                f"Respond with a JSON object where each key is a zipcode and the value is an object with 'city' and 'state' properties."}
                ],
                max_retries=2
            )

            print(f"Raw API response: {response}")

            if isinstance(response, BatchLocationInfo):
                batch_location_info = response.locations
            elif isinstance(response, BatchLocationList):
                batch_location_info = {item.zipcode: item.to_location_info() for item in response.root}
            else:
                raise ValueError("Unexpected response format")

            # Ensure all requested zipcodes are in the response
            for zipcode in zipcodes:
                if zipcode not in batch_location_info:
                    print(f"WARNING: Zipcode {zipcode} not found in API response. Adding default values.")
                    batch_location_info[zipcode] = LocationInfo(city="Unknown", state="Unknown")

            for zipcode, info in batch_location_info.items():
                print(f"Location info for {zipcode}: {info}")

            print(f"Successfully retrieved location info for {len(batch_location_info)} zipcodes")
            return batch_location_info

        except Exception as e:
            print(f"ERROR: Error calling OpenAI API: {e}")
            import traceback
            print(traceback.format_exc())
            return {zipcode: LocationInfo(city="Unknown", state="Unknown") for zipcode in zipcodes}
