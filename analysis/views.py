import os
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Video

from footage_parser.video_analyser import VideoAnalyser
from footage_parser.vprofile import Profile


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

    analyser = VideoAnalyser(video.id, video.video_file.path, "person")
    analyser.save_profile_screenshots()
    profiles = analyser.get_profile_data_for_recognition()


    return JsonResponse({
        'message': 'Video uploaded successfully',
        'video_id': video.id,
        'video_url': video.video_file.url,
        'profiles': profiles
    }, status=201)


@csrf_exempt
def get_video_clips(request):
        data = json.loads(request.body)

        profile_id = data.get('profile_id', 0)
        video_id = data.get('video_id', 0)
        profile_path = f"{video_id}/profile_{video_id}"

        profile = Profile(id=profile_id)
        profile.load_from_json(profile_path)
        profile.save_video_clips(path=profile_path, padding_seconds=3)
        vid_clips = profile.get_video_clips_paths()
        
        return JsonResponse({
            'video_clips': vid_clips
        }, status=200)