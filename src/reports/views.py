from django.http import HttpResponse
from django.http import JsonResponse
from django.template.loader import get_template
from django.views.generic import ListView, DetailView
from profiles.models import Profile
from xhtml2pdf import pisa

from .models import Report
from .utils import get_report_image


# Create your views here.
class ReportListView(ListView):
    model = Report
    template_name = 'reports/main.html'


class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/detail.html'


def create_report_view(request):
    if request.is_ajax():
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = request.POST.get('image')

        img = get_report_image(image)

        # author = Profile.objects.get(user = request.user)
        if request.user.is_authenticated:
            author = Profile.objects.get(user_id=request.user.id)
        else:
            print("bbbbbbb")
        Report.objects.create(name=name, remarks=remarks, image=img, author=author)
        return JsonResponse({'msg': 'send'})
    return JsonResponse({'msg': 'not send ok'})


def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'
    obj2 = Report.objects.get(pk=pk)
    obj = Report.objects.get(pk=pk)

    # obj = get_object_or_404(Report,pk=pk)
    context = {'obj': obj}
    # 声明一个django的response，定义content_type
    response = HttpResponse(content_type='application/pdf')
    # 如果download，设置这个属性 attachment用来表示是否保存
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    # 用render 方法将content 内容放进网页
    temlate = get_template(template_path)
    html = temlate.render(context)

    # 声明一个pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response
    )
    if pisa_status.err:
        return HttpResponse('pdf Errors' + html)
    return response
