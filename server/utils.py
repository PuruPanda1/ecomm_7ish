from orders.models import Order 
from product.models import ProductVariant
from orders.models import OrderItem
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncDay
from datetime import date, timedelta
import json
from collections import defaultdict
from decimal import Decimal
from django.db.models import Sum, Count

# order data for chart
def get_order_chart(request):
    end_date = date.today()
    start_date = end_date - timedelta(days=27)

    orders_per_day = (
        Order.objects.filter(order_date__date__range=[start_date, end_date])
        .annotate(day=TruncDay('order_date'))
        .values('day')
        .annotate(order_count=Count('id'))
        .order_by('day')
    )

    labels = []
    count = []

    for i in range(28):
        day = start_date + timedelta(days=i) 
        labels.append(day.strftime("%d/%m"))  
        
        # Convert order day to a date before comparison
        day_count = next((item['order_count'] for item in orders_per_day if item['day'].date() == day), 0)
        
        count.append(day_count)



    chart = {
        "labels": labels,
        "datasets": [{"data": count, "borderColor": "#f43f5e"}]
    }
    json_chart = json.dumps(chart)
    return json_chart

# revenue data for chart
def get_revenue_chart(request):
    end_date = date.today()
    start_date = end_date - timedelta(days=27)

    orders = Order.objects.filter(order_date__date__range=[start_date, end_date])

    revenue_per_day = defaultdict(Decimal)

    for order in orders:
        order_day = order.order_date.date()  # Convert to date object
        revenue_per_day[order_day] += order.total_price_pre_tax  # Aggregate revenue per day

    labels = []
    count = []

    for i in range(28):
        day = start_date + timedelta(days=i)
        labels.append(day.strftime("%d/%m"))  # Format date as "DD/MM"
        
        # Get revenue for the day or default to 0
        day_revenue = revenue_per_day.get(day, Decimal(0))
        
        count.append(float(day_revenue))  # Convert Decimal to float for JSON serialization

    chart = {
        "labels": labels,
        "datasets": [{"data": count, "borderColor": "#3b82f6"}]
    }
    json_chart = json.dumps(chart)
    return json_chart

# get top 5 sold products in last 28 days
def get_top_products(request):
    end_date = date.today()
    start_date = end_date - timedelta(days=27)

    top_selling_products = (
        OrderItem.objects.filter(order__order_date__date__range=[start_date, end_date])
        .values('product_variant__product__name')  # Group by product name
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:5]  # Order by highest sales and limit to 5
    )

    top_products_list = []
    for product in top_selling_products:
        top_products_list.append({"title": product['product_variant__product__name'],"description": f"{product['total_sold']} Nos" ,"value": product['total_sold']})

    return top_products_list


def get_avg_chart():
    # Date range: last 28 days including today
    end_date = date.today()
    start_date = end_date - timedelta(days=27)

    # Fetch delivered and returned orders within the date range
    delivered_orders = Order.objects.filter(order_status='delivered', order_date__date__range=[start_date, end_date])
    returned_orders = Order.objects.filter(order_status='returned', order_date__date__range=[start_date, end_date])

    # Compute revenue per day manually since total_price_pre_tax is a property
    delivered_revenue = defaultdict(Decimal)
    returned_revenue = defaultdict(Decimal)

    for order in delivered_orders:
        day = order.order_date.date()
        delivered_revenue[day] += order.total_price_pre_tax  # Property access

    for order in returned_orders:
        day = order.order_date.date()
        returned_revenue[day] += order.total_price_pre_tax  # Property access

    # Compute total revenue and average per day
    all_orders = Order.objects.filter(order_date__date__range=[start_date, end_date])
    total_revenue = sum(order.total_price_pre_tax for order in all_orders)
    total_days = (end_date - start_date).days + 1
    average_revenue = total_revenue / total_days if total_days else 0

    # Prepare labels and datasets
    labels, positive, negative, average = [], [], [], []

    for i in range(28):
        day = start_date + timedelta(days=i)
        labels.append(day.strftime("%d/%m"))  # Format as "DD/MM"

        # Get revenue values or default to 0
        positive.append(float(delivered_revenue.get(day, 0)))
        negative.append(float(returned_revenue.get(day, 0)*-1))
        average.append(float(average_revenue))

    # Construct chart data
    chart = {
        "labels": labels,
        "datasets": [
            {
                "label": "Average Revenue",
                "type": "line",
                "data": average,
                "backgroundColor": "#f0abfc",
                "borderColor": "#f0abfc",
            },
            {
                "label": "Delivered Orders Revenue",
                "data": positive,
                "backgroundColor": "#9333ea",
            },
            {
                "label": "Returned Orders Revenue",
                "data": negative,
                "backgroundColor": "#f43f5e",
            },
        ],
    }
    chart_data = json.dumps(chart)
    return chart_data