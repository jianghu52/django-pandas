from profiles.models import Profile
from django.http import JsonResponse
from .models import Report
from .utils import get_report_image


# Create your views here.

def create_report_view(request):
    if request.is_ajax():
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = request.POST.get('image')

        img = get_report_image(image)

        # author = Profile.objects.get(user = request.user)
        if request.user.is_authenticated:
            author = Profile.objects.get(user_id=request.user.id)
            print('aaaaa')
        else:
            print("bbbbbbb")
        Report.objects.create(name=name, remarks=remarks, image=img, author=author)
        return JsonResponse({'msg': 'send'})
    return JsonResponse({'msg': 'not send ok'})
