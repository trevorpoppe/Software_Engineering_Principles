import math

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def match_closest_points(array1, array2):
    matches = []
    for lat1, lon1 in array1:
        min_distance = float('inf')
        closest_point = None
        for lat2, lon2 in array2:
            distance = haversine(lat1, lon1, lat2, lon2)
            if distance < min_distance:
                min_distance = distance
                closest_point = (lat2, lon2)
        matches.append((lat1, lon1, closest_point, min_distance))
    return matches

# Example usage
array1 = [(42.3601, -71.0589), (40.7128, -74.0060)]  # Boston, NYC
array2 = [(34.0522, -118.2437), (37.7749, -122.4194)]  # LA, SF

matches = match_closest_points(array1, array2)
for match in matches:
    print(f"Point {match[0:2]} is closest to {match[2]} with a distance of {match[3]:.2f} km")

# This script includes code and ideas generated with the assistance of ChatGPT, developed by OpenAI.
# Date: 22 January 2025
