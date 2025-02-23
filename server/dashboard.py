import random
import json
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from orders.models import Order
from product.models import Product
from django.utils import timezone
from datetime import timedelta
from .utils import *

def dashboard_callback(request, context):
    WEEKDAYS = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]

    positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
    negative = [[-1, -random.randrange(8, 28)] for i in range(1, 28)]
    average = [r[1] - random.randint(3, 5) for r in positive]

    # Top cards count data
    orders = Order.objects.filter(order_status='delivered')
    revenue = orders.aggregate(Sum('total_price_pre_tax'))['total_price_pre_tax__sum'] or 0
    order_count = orders.count()
    pending_order_count = Order.objects.filter(order_status__in=['ordered','confirmed', 'shipped']).count()
    return_count = Order.objects.filter(order_status__in=['refunded','returned']).count()

    product_count = Product.objects.filter(is_active=True).count()
    
    last_week_revenue = orders.filter(
        order_date__gte=timezone.now() - timedelta(days=7)
        ).aggregate(Sum('total_price_pre_tax'))['total_price_pre_tax__sum'] or 0
    print(f"Revenue = {revenue}")
    print(f"Last Week Revenue = {last_week_revenue}")

    last_week_orders = orders.filter(order_date__gte=timezone.now() - timedelta(days=7)).count()
    
    order_chart = get_order_chart(request)
    revenue_chart = get_revenue_chart(request)

    top_products_list = get_top_products(request)
    chart_data = get_avg_chart()
    
    context.update(
        {
            "kpi": [
                {
                    "title": "Revenue",
                    "metric": f"Rs. {revenue}",
                },
                {
                    "title": "Total Orders",
                    "metric": order_count,
                },
                {
                    "title": "Pending Orders",
                    "metric": pending_order_count,
                },
                {
                    "title": "Returns",
                    "metric": return_count,
                },
                {
                    "title": "Total Products",
                    "metric": f"{product_count} Nos",
                },
            ],
            # print the top 5 products according to sold quantity
            "progress": top_products_list,
            "chart": chart_data,
            "performance": [
                {
                    "title": _("Last month revenue"),
                    "metric": f"Rs. {last_week_revenue}",
                    "footer": mark_safe(
                        '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                    ),
                    "chart": revenue_chart,
                },
                {
                    "title": _("Last month orders"),
                    "metric": last_week_orders,
                    "footer": mark_safe(
                        '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                    ),
                    "chart": order_chart,
                },
            ]
        },
    )

    return context