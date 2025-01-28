import unittest
# from unittest.mock import patch
from Project1_GeoLocationMatching.geo_matching import haversine, match_closest_points, get_coordinates_from_user


class TestHaversine(unittest.TestCase):
    def test_haversine(self):
        # Known test case: distance between (0, 0) and (0, 1)
        lat1, lon1 = 0, 0
        lat2, lon2 = 0, 1
        expected_distance = 111.195  # Approximate distance in km
        result = haversine(lat1, lon1, lat2, lon2)
        self.assertAlmostEqual(result, expected_distance, places=3)

class TestMatchClosestPoints(unittest.TestCase):
    def test_match_closest_points(self):
        array1 = [(0, 0), (1, 1)]
        array2 = [(0, 1), (1, 0)]
        
        # Expected result: (0, 0) is closest to (0, 1) with a distance of ~111.195
        # (1, 1) is closest to (1, 0) with a distance of ~111.195
        expected_matches = [
            ((0, 0), (0, 1), 111.195),
            ((1, 1), (1, 0), 111.195)
        ]
        
        matches = match_closest_points(array1, array2)
        
        for i, match in enumerate(matches):
            self.assertAlmostEqual(match[3], expected_matches[i][2], places=3)
            self.assertEqual(match[2], expected_matches[i][1])

class TestGetCoordinatesFromUser(unittest.TestCase):
    @patch('builtins.input', side_effect=['12.34,56.78', '98.76,54.32', 'done'])
    def test_get_coordinates_from_user(self, mock_input):
        expected_coordinates = [(12.34, 56.78), (98.76, 54.32)]
        result = get_coordinates_from_user()
        self.assertEqual(result, expected_coordinates)

    @patch('builtins.input', side_effect=['invalid_input', '12.34,56.78', 'done'])
    def test_get_coordinates_from_user_invalid_input(self, mock_input):
        expected_coordinates = [(12.34, 56.78)]
        result = get_coordinates_from_user()
        self.assertEqual(result, expected_coordinates)

if __name__ == '__main__':
    unittest.main()
