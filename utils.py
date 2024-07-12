import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6378.137  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c * 1000  # Return in meters

def total_distance(coords):
    total_dist = 0.0
    for i in range(1, len(coords)):
        lat1, lon1 = coords[i - 1]
        lat2, lon2 = coords[i]
        distance = haversine(lat1, lon1, lat2, lon2)
        if distance > 0.05 and distance < 3.1:
            total_dist += distance
        else:
            pass
    return total_dist
