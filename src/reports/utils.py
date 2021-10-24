import base64,uuid
from django.core.files.base import ContentFile

def get_report_image(data):
    f, str_image = data.split(';base64')
    decode_img = base64.b64decode(str_image)
    img_name = str(uuid.uuid4())[:10] + '.png'
    data = ContentFile(decode_img,name=img_name)
    return data