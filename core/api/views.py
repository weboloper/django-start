from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from core.forms import AttachmentUploadForm
from core.models import Attachment
from django import forms
from django.db import IntegrityError
from django.conf import settings
from django.contrib.sites.models import Site

@csrf_exempt
def upload_attachment_url(request):
        
    if request.method == "POST":
        try:
            domain = Site.objects.get_current().domain
            attachment = Attachment.objects.create(guid=request.FILES['file'])
            attachment_url = 'http://' + domain + attachment.guid.url 
            return JsonResponse({'location':attachment_url  })
        except ValueError as e: 
            return JsonResponse({'error': True, 'errors': str(e) })
    