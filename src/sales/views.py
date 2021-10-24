import pandas as pd
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from reports.forms import ReportForm

from .forms import SalesSearchForm
from .models import Sale
from .utils import get_customer_from_id, get_salesman_from_id, get_chart


# Create your views here.

def home_view(request):
    """
    路由的时候，会调用home_view的方法
    :param request: 路由的request
    :return: 调用rend 方法，包含了返回的html，以及编辑好的context变量
    """

    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()
    sales_df = None
    positions_df = None
    merged_df = None
    df = None
    chart = None
    no_data = None
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')

        # 开始使用pandas
        sale_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        if len(sale_qs) > 0:
            sales_df = pd.DataFrame(sale_qs.values())
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df['updated'] = sales_df['updated'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df.rename({'salesman_id': 'salesman', 'customer_id': 'customer', 'id': 'sales_id'}, axis=1,
                            inplace=True)
            # sales_df['sales_id'] = sales_df['id']
            # 追加新字段
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
            # 合并表
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')
            df = merged_df.groupby('transaction_id', as_index=False)['price'].agg('sum')

            chart = get_chart(chart_type, sales_df, results_by)

            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()

        else:
            no_data = 'No data is available in this date range'


    context = {
        'search_form': search_form,
        'report_form': report_form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'df': df,
        'chart': chart,
        'no_data': no_data,

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
