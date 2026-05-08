import json
from datetime import datetime, timedelta
from geopy.distance import geodesic

def load_routes():
    """Load mock routes from JSON file"""
    with open('data/mock_routes.json', 'r') as f:
        return json.load(f)

def get_route(route_id):
    """Get route by ID"""
    routes = load_routes()
    for route in routes:
        if route['route_id'] == route_id:
            return route
    return None

def calculate_gps_staleness(gps_timestamp_str):
    """
    Calculate how stale GPS data is in minutes.
    """
    gps_timestamp = datetime.fromisoformat(gps_timestamp_str.replace('Z', '+00:00'))
    now = datetime.now(gps_timestamp.tzinfo)
    age_seconds = (now - gps_timestamp).total_seconds()
    return int(age_seconds / 60)

def calculate_precision_eta(order):
    """
    Calculate precision ETA based on GPS location, traffic, remaining stops.

    Returns: {
        'eta_start': datetime string,
        'eta_end': datetime string,
        'confidence': float (0-1),
        'gps_staleness_min': int,
        'escalation_triggered': bool,
        'escalation_reason': str or None,
        'calculation_details': dict
    }
    """
    route = get_route(order['route_id'])

    if not route:
        return {
            'escalation_triggered': True,
            'escalation_reason': 'Route not found in system',
            'confidence': 0.0
        }

    # Get GPS data from route
    gps = route['current_location']
    gps_age_min = calculate_gps_staleness(gps['timestamp'])

    # Check GPS staleness threshold
    if gps_age_min > 30:
        return {
            'escalation_triggered': True,
            'escalation_reason': f'GPS data stale ({gps_age_min} min > 30 min threshold)',
            'confidence': 0.0,
            'gps_staleness_min': gps_age_min
        }

    # Calculate distance from current location to delivery address
    driver_location = (gps['lat'], gps['lon'])
    delivery_location = (order['delivery_address_lat'], order['delivery_address_lon'])
    distance_km = geodesic(driver_location, delivery_location).kilometers

    # Traffic multiplier (mock: 1.15 for moderate traffic)
    traffic_multiplier = 1.15

    # Calculate travel time (assume 50 km/h average city speed)
    travel_time_min = (distance_km / 50) * 60 * traffic_multiplier

    # Add stop duration (remaining stops × 15 min average)
    stop_duration_min = route['remaining_stops'] * 15

    # Total ETA = travel time + stop duration
    total_eta_min = travel_time_min + stop_duration_min

    # Calculate ETA window (±15 min)
    now = datetime.now()
    eta_start = now + timedelta(minutes=int(total_eta_min - 15))
    eta_end = now + timedelta(minutes=int(total_eta_min + 15))

    # Confidence scoring (degrades with GPS age)
    confidence = min(0.95 - (gps_age_min / 30) * 0.25, 1.0)

    return {
        'eta_start': eta_start.strftime('%H:%M'),
        'eta_end': eta_end.strftime('%H:%M'),
        'eta_start_full': eta_start.isoformat(),
        'eta_end_full': eta_end.isoformat(),
        'confidence': round(confidence, 2),
        'gps_staleness_min': gps_age_min,
        'escalation_triggered': False,
        'escalation_reason': None,
        'calculation_details': {
            'distance_km': round(distance_km, 2),
            'travel_time_min': round(travel_time_min, 1),
            'stop_duration_min': stop_duration_min,
            'traffic_multiplier': traffic_multiplier,
            'driver_location': gps['location_name'],
            'remaining_stops': route['remaining_stops']
        }
    }

def get_standard_eta(order):
    """
    Get standard scheduled ETA window (simple lookup).

    Returns: {
        'eta_window': string,
        'delegation_level': 'FULLY_AGENTIC'
    }
    """
    return {
        'eta_window': f"{order['scheduled_eta_start']}-{order['scheduled_eta_end']}",
        'eta_start': order['scheduled_eta_start'],
        'eta_end': order['scheduled_eta_end'],
        'delegation_level': 'FULLY_AGENTIC'
    }
