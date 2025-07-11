from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .models import DispatchTask

@require_GET
def list_dispatch_tasks(request):
    try:
        tasks = DispatchTask.objects.select_related(
            'dispatcher__user', 'driver__user', 'vehicle', 'route', 'trip'
        ).all()

        task_data = []
        for task in tasks:
            task_data.append({
                "id": task.id,
                "dispatcher": task.dispatcher.user.username if task.dispatcher and task.dispatcher.user else None,
                "driver": task.driver.user.username if task.driver and task.driver.user else None,
                "vehicle": task.vehicle.license_plate,
                "trip_id": task.trip.id,
                "route_id": task.route.id,
                "created_at": task.created_at.isoformat()
            })

        return JsonResponse({"dispatch_tasks": task_data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
