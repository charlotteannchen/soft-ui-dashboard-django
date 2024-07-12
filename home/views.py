from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):

    # Page from the theme 
    return render(request, 'pages/index.html')


# from django.http import JsonResponse
# from django.core.files.storage import FileSystemStorage


# def upload(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         image = request.FILES['image']
#         fs = FileSystemStorage()
#         filename = fs.save(image.name, image)
#         uploaded_file_url = fs.url(filename)
#         return JsonResponse({'uploaded_file_url': uploaded_file_url})
#     return render(request, 'pages/index.html')

from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import shutil

def upload(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        # Save image to media folder first
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        # Move file from media to static/uploads
        static_uploads_path = settings.UPLOAD_TO_STATIC_DIR
        new_file_path = os.path.join(static_uploads_path, filename)
        shutil.move(os.path.join(settings.MEDIA_ROOT, filename), new_file_path)

        # Get the static URL of the uploaded file
        static_file_url = f"{settings.STATIC_URL}uploads/{filename}"
        return JsonResponse({'uploaded_file_url': static_file_url})
    return JsonResponse({'error': 'Invalid request'}, status=400)