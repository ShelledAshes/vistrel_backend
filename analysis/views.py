import os


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Video


# Create your views here.
def home(request):

    data = {
        "message": "Welcome to Django Server",
        "status": "success"
    }

    return JsonResponse(data)


@csrf_exempt
def upload_video(request):

    if request.method != 'POST':
        return JsonResponse({
            'error': 'Only POST requests are allowed'
        }, status=405)

    video_file = request.FILES.get('video')

    if not video_file:
        return JsonResponse({
            'error': 'No video file received'
        }, status=400)

    video = Video.objects.create(
        title=os.path.splitext(video_file.name)[0],
        video_file=video_file
    )

    return JsonResponse({
        'message': 'Video uploaded successfully',
        'id': video.id,
        'file': video.video_file.url
    }, status=201)