from dto.FileDto import FileDto
from geopy.geocoders import MapQuest

from util.Util_IO import Util_IO


class GeoLocator:
    known_locations = {}

    def __init__(self, fileDto:FileDto):
        self.fileDto = fileDto
        # self.geolocator = Nominatim(user_agent="scanner")
        self.geolocator = MapQuest("SGc34ZYmjUpexPdGxqWRWTPeh2gb7de5")
        GeoLocator.known_locations = Util_IO.read_known_locations()

    def get_location(self):
        location = None
        if self.fileDto.image_meta_data:
            try:

                # Assuming it's there get lat and long from image_data_data, 5hsr!B9jSS4H
                # If it turns out to be impossible, then delete this class

                # Assign Latitude & Longitude (when getting from image meta data, we may have to convert str to float
                Latitude = 25.594095
                Longitude = 85.137566

                # Goal is to eventually get lat/long from image file, so go ahead and round values
                # The goal of rounding is to limit size of GeoLocator.known_locations by limiting precision of lat/long
                Latitude = round(Latitude,4)
                Longitude = round(Longitude,4)

                # Displaying Latitude and Longitude
                # print("Latitude: ", Latitude)
                # print("Longitude: ", Longitude)

                location_key = str(Latitude) + "," + str(Longitude)

                # If lat/long exists in saved Dict, then used saved value, dont' look it up.
                if location_key in GeoLocator.known_locations:
                    return GeoLocator.known_locations[location_key]

                # Get location with geocode
                # location = geolocator.geocode(Latitude + "," + Longitude)
                location = self.geolocator.reverse(location_key)

                # Add new location to saved location dict
                GeoLocator.known_locations[location_key] = location.address

                # Save to file system for use on next run
                Util_IO.save_known_locations(GeoLocator.known_locations)

            except Exception as e:
                print("Error geolocator",str(e))
                location = "Error geolocator"+str(e)

        return location
