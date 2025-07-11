from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from orders.models import Order
from billing.models import Payment  # if you store payments in DB
from django.db.models import Sum

@require_http_methods(["GET"])
def accountant_dashboard(request):
    try:
        total_orders = Order.objects.count()
        completed_orders = Order.objects.filter(status='completed').count()
        pending_orders = Order.objects.filter(status='pending').count()
        cancelled_orders = Order.objects.filter(status='cancelled').count()

        # Sum of amounts from completed payments
        total_revenue = Payment.objects.filter(status='completed').aggregate(total=Sum('amount'))['total'] or 0

        # Unpaid orders
        unpaid_orders = Payment.objects.filter(status='pending').count()

        # Average revenue per order
        avg_revenue_per_order = round(total_revenue / completed_orders, 2) if completed_orders else 0

        return JsonResponse({
            "metrics": {
                "total_orders": total_orders,
                "completed_orders": completed_orders,
                "pending_orders": pending_orders,
                "cancelled_orders": cancelled_orders,
                "unpaid_orders": unpaid_orders,
                "total_revenue_usd": float(total_revenue),
                "average_revenue_per_order_usd": float(avg_revenue_per_order)
            }
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
