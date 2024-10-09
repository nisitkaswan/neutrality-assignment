import os
from typing import List, Dict
import instructor
from django.conf import settings
from pydantic import BaseModel, Field
from openai import OpenAI

class LocationInfo(BaseModel):
    city: str
    state: str

class BatchLocationInfo(BaseModel):
    locations: Dict[str, LocationInfo] = Field(default_factory=dict)

class LocationService:
    def __init__(self):
        self.client = instructor.from_openai(OpenAI(api_key=settings.OPENAI_API_KEY))
        print("LocationService initialized")

    def get_location_info(self, zipcode: str) -> LocationInfo:
        """Get the city and state for a given US zipcode."""
        print(f"Getting location info for zipcode: {zipcode}")
        return self.get_batch_location_info([zipcode])[zipcode]

    def get_batch_location_info(self, zipcodes: List[str]) -> Dict[str, LocationInfo]:
        """Get the city and state for a batch of US zipcodes."""
        print(f"Getting batch location info for {len(zipcodes)} zipcodes")
        try:
            zipcodes_str = ", ".join(zipcodes)
            print(f"Zipcodes: {zipcodes_str}")

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                response_model=BatchLocationInfo,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides location information."},
                    {"role": "user", "content": f"For each of the following US zipcodes, provide the city and state: {zipcodes_str}. Respond with a JSON object where each key is a zipcode and the value is an object with 'city' and 'state' properties. For example: \n\n```json\n{{\"94040\": {{\"city\": \"Mountain View\", \"state\": \"CA\"}}}}\n```"}
                ],
                max_retries=2
            )

            print(f"Raw API response: {response}")

            # Access the locations directly from the response object
            batch_location_info = response.locations

            # Handle potential errors in the response
            if not batch_location_info:
                print("ERROR: Empty or invalid response from OpenAI API")
                return {zipcode: LocationInfo(city="Unknown", state="Unknown") for zipcode in zipcodes}

            # Print and return the results
            for zipcode, info in batch_location_info.items():
                print(f"Location info for {zipcode}: city={info.city}, state={info.state}")

            print(f"Successfully retrieved location info for {len(batch_location_info)} zipcodes")
            return batch_location_info

        except Exception as e:
            print(f"ERROR: Error calling OpenAI API: {e}")
            import traceback
            print(traceback.format_exc())
            return {zipcode: LocationInfo(city="Unknown", state="Unknown") for zipcode in zipcodes}