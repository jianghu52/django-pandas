from django.db import models
from django.db.models.base import Model
from profiles.models import Profile
from django.http import JsonResponse
from .models import Report
from .utils import get_report_image
from django.views.generic import ListView,DetailView


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
