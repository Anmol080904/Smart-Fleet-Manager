# dispatch/utils.py
from vehicles.models import Vehicle
from trips.models import Trip

def get_optimal_vehicle_only():
    vehicles = Vehicle.objects.filter(status='active').distinct()
    for v in vehicles:
        if not Trip.objects.filter(vehicle=v, end_time__isnull=True).exists():
            return v
    return None
