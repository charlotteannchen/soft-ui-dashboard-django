from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .forms import UploadForm
import os
import shutil
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'pages/index.html')

def upload(request):
    if request.method == 'POST':
        logger.debug("POST request received")
        logger.debug(f"Request POST data: {request.POST}")
        logger.debug(f"Request FILES data: {request.FILES}")

        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            
            # Check if either image or message is provided
            if not upload.image and not upload.message:
                logger.error("No image or message provided")
                return JsonResponse({'error': 'At least one of the fields (image or message) is required.'}, status=400)
            
            upload.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                logger.debug("AJAX request detected")
                
                # Save image to media folder first
                if upload.image:
                    try:
                        image = upload.image
                        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                        filename = fs.save(image.name, image)
                        uploaded_file_url = fs.url(filename)

                        # Move file from media to static/uploads
                        static_uploads_path = os.path.join(settings.STATICFILES_DIRS[0], 'uploads')
                        os.makedirs(static_uploads_path, exist_ok=True)
                        new_file_path = os.path.join(static_uploads_path, filename)
                        shutil.move(os.path.join(settings.MEDIA_ROOT, filename), new_file_path)

                        # Get the static URL of the uploaded file
                        static_file_url = f"{settings.STATIC_URL}uploads/{filename}"
                    except Exception as e:
                        logger.error(f"Error processing image: {e}")
                        return JsonResponse({'error': 'There was an error processing the uploaded image. Please try again.'}, status=400)
                else:
                    static_file_url = None

                return JsonResponse({
                    'uploaded_file_url': static_file_url,
                    'extra_message': upload.message
                })
            else:
                return render(request, 'pages/index.html', {
                    'form': UploadForm(),
                    'success': True
                })
        else:
            logger.error("Form is invalid")
            logger.error(f"Form errors: {form.errors}")
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Invalid form data', 'form_errors': form.errors}, status=400)
            else:
                return render(request, 'pages/index.html', {
                    'form': form,
                    'errors': form.errors
                })
    else:
        form = UploadForm()
        logger.debug("GET request received")

    return render(request, 'pages/index.html', {'form': form})
