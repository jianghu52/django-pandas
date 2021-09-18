import pandas as pd
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .forms import SalesSearchForm
from .models import Sale
from .utils import get_customer_from_id, get_salesman_from_id


# Create your views here.

def home_view(request):
    form = SalesSearchForm(request.POST or None)
    sales_df = None
    positions_df = None
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_types = request.POST.get('chart_type')

        sale_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        if len(sale_qs) > 0:
            sales_df = pd.DataFrame(sale_qs.values())
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df['updated'] = sales_df['updated'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df.rename({'salesman_id': 'salesman', 'customer_id': 'customer'}, axis=1, inplace=True)

            positions_data = []
            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj = {
                        'positions_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id()
                    }
                    positions_data.append(obj)
            positions_df = pd.DataFrame(positions_data)
            print(positions_df)
            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            print(sales_df)
        else:
            print("no data")

    context = {
        'form': form,
        'sales_df': sales_df,
        'positions_df': positions_df
    }
    return render(request, 'sales/home.html', context)


class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'


class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'


def sale_list_view(request):
    qs = Sale.objects.all()
    return render(request, 'sales/main.html', {'qs': qs})


def sale_detail_view(request, **kwargs):
    pk = kwargs.get('pk')
    obj = Sale.objects.get(pk=pk)
    return render(request, 'sales/detail.html', {'object': obj})
