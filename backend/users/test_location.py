import os
import django


from users.services.location import LocationService  # Adjust the import path as needed

def test_location_service():
    # Initialize the LocationService
    location_service = LocationService()

    # Test single zipcode lookup
    single_zipcode = "90210"
    print(f"\nTesting single zipcode lookup for {single_zipcode}")
    single_result = location_service.get_single_location_info(single_zipcode)
    print(f"Result: {single_result}")

    # Test batch zipcode lookup
    batch_zipcodes = ["10001", "60601", "90210", "75001", "20001"]
    print(f"\nTesting batch zipcode lookup for {batch_zipcodes}")
    batch_results = location_service.get_batch_location_info(batch_zipcodes)
    for zipcode, info in batch_results.items():
        print(f"Zipcode: {zipcode}, City: {info.city}, State: {info.state}")

    # # Test with an invalid zipcode
    # invalid_zipcode = "00000"
    # print(f"\nTesting invalid zipcode: {invalid_zipcode}")
    # invalid_result = location_service.get_location_info(invalid_zipcode)
    # print(f"Result for invalid zipcode: {invalid_result}")

if __name__ == "__main__":
    test_location_service()