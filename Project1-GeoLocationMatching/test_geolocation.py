import unittest
from your_module import haversine, match_closest_points  # Replace 'your_module' with the actual module name if needed

class TestGeoFunctions(unittest.TestCase):

    def test_haversine(self):
        # Test with known values (Boston to NYC)
        lat1, lon1 = 42.3601, -71.0589  # Boston
        lat2, lon2 = 40.7128, -74.0060  # NYC
        distance = haversine(lat1, lon1, lat2, lon2)
        
        # Using a known approximate distance between Boston and NYC
        self.assertAlmostEqual(distance, 306.22, places=2)

    def test_match_closest_points(self):
        # Test with simple example
        array1 = [(42.3601, -71.0589), (40.7128, -74.0060)]  # Boston, NYC
        array2 = [(34.0522, -118.2437), (37.7749, -122.4194)]  # LA, SF
        matches = match_closest_points(array1, array2)
        
        # Check that the closest match for Boston is LA, and for NYC is SF
        self.assertEqual(matches[0][2], (34.0522, -118.2437))  # Boston -> LA
        self.assertEqual(matches[1][2], (37.7749, -122.4194))  # NYC -> SF

        # Check the distance values are reasonable
        self.assertGreater(matches[0][3], 0)
        self.assertGreater(matches[1][3], 0)

if __name__ == '__main__':
    unittest.main()
