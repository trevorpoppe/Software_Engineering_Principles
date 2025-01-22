import unittest
from geo_matching import haversine  # Update this based on your function location

class TestGeoFunctions(unittest.TestCase):

    def test_haversine(self):
        # Example test for the haversine function
        lat1, lon1 = 42.3601, -71.0589  # Boston
        lat2, lon2 = 40.7128, -74.0060  # NYC
        expected_distance = 306.22  # Replace with your expected value
        self.assertAlmostEqual(haversine(lat1, lon1, lat2, lon2), expected_distance, places=2)

if __name__ == '__main__':
    unittest.main()
