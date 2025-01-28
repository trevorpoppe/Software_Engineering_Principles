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

def get_coordinates_from_user():
    coordinates = []
    print("Enter coordinates in the format 'latitude,longitude'. Type 'done' when finished:")
    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "done":
            break
        try:
            lat, lon = map(float, user_input.split(","))
            coordinates.append((lat, lon))
        except ValueError:
            print("Invalid input. Please enter coordinates in the format 'latitude,longitude'.")
    return coordinates

def main():
    print("Choose an option:")
    print("1. Enter coordinates manually")
    print("2. Upload arrays from a file")

    choice = input("> ").strip()
    if choice == "1":
        print("Enter coordinates for the first array:")
        array1 = get_coordinates_from_user()
        print("Enter coordinates for the second array:")
        array2 = get_coordinates_from_user()
    elif choice == "2":
        try:
            file1 = input("Enter the filename for the first array: ").strip()
            file2 = input("Enter the filename for the second array: ").strip()
            with open(file1, "r") as f1, open(file2, "r") as f2:
                array1 = [tuple(map(float, line.strip().split(","))) for line in f1]
                array2 = [tuple(map(float, line.strip().split(","))) for line in f2]
        except FileNotFoundError:
            print("File not found. Please check the filenames and try again.")
            return
        except ValueError:
            print("File contents must be in the format 'latitude,longitude' per line.")
            return
    else:
        print("Invalid choice. Exiting.")
        return

    matches = match_closest_points(array1, array2)
    print("\nResults:")
    for match in matches:
        print(f"Point {match[0:2]} is closest to {match[2]} with a distance of {match[3]:.2f} km")

if __name__ == "__main__":
    main()
# This script includes code and ideas generated with the assistance of ChatGPT, developed by OpenAI.
# ChatGPT was used to enhance functionality and improve user interaction.
# Date: 24 January 2025
