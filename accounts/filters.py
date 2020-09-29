import django_filters
#from django_filters import DateFilter, CharFilter, NumberFilter
import datetime

from .models import *
"""
class OrderFilter(django_filters.FilterSet):
	#start_date = DateFilter(field_name="DueDate", lookup_expr='gte')
	#end_date = DateFilter(field_name="DueDate", lookup_expr='lte')

	#start_Price = NumberFilter(field_name="Price", lookup_expr='gte')
	#end_Price = NumberFilter(field_name="Price", lookup_expr='lte')

	#DateCreated = Order.objects.filter(DateCreated__contains=datetime.date(1986, 7, 28))

	class Meta:
		model = Order
		fields = ['Outlet', 'status','is_paid']
"""