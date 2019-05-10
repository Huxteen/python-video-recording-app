from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from collections import Counter
from django.shortcuts import render, redirect
from dashboard.models import VideoRecord
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


# Process and redirect login form data
@login_required(login_url="/accounts/login")
def dashboard(request):
    if request.method == "POST":
        upload_video = VideoRecord()
        upload_video.video_name = request.FILES['video_name']
        user_id = int(request.user.id)
        upload_video.user_id = User(pk=user_id)
        upload_video.admin_id = None
        upload_video.status = False
        upload_video.updated_at = timezone.datetime.now()
        upload_video.created_at = timezone.datetime.now()
        upload_video.save()
        status = VideoRecord.objects.latest('created_at')


        # send_mail(subject, message, from_email, to_list, fail_silently=True)
        subject = 'A new video is available for review'

        # current_site = "https://quick-loan.herokuapp.com/dashboard/approve-loan"
        current_site = str(get_current_site(request)) + '/dashboard/review-video'
        uid = (status.id)

        activation_link = "{0}/{1}".format(current_site, uid)
        message = "Hello {0},\n {1}\n \n{2}".format("Admin", subject, activation_link)

        # message = 'Welcome to Quickcash Loan. In order to gain full access to our website please activate your account with the link below.'
        from_email = settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list)



        data = {
            'message': 'Video has been added uploaded successfully',
            'status': 'success',
            'video_name': str(status.video_name),
            'id': status.id,
            'user_id': str(status.user_id),
        }
        return JsonResponse(data)
    video_data = VideoRecord.objects.all()
    context = {'video_data': video_data}
    return render(request, 'dashboard/dashboard.html', context)



@login_required(login_url="/accounts/login")
def my_videos(request):
    user = int(request.user.id)
    my_videos = VideoRecord.objects.filter(user_id=user).order_by('-created_at')
    context = {'my_videos': my_videos}
    return render(request, 'dashboard/my_videos.html', context)

@login_required(login_url="/accounts/login")
def view_all_video(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    all_videos = VideoRecord.objects.all().order_by('-created_at')
    context = {'all_videos': all_videos}
    return render(request, 'dashboard/view_all_video.html', context)


@login_required(login_url="/accounts/login")
def delete_video(request, video_id):
    if request.method == 'POST':
        delete_video = VideoRecord.objects.get(pk=video_id)
        delete_video.delete()
        messages.warning(request, 'Video has been deleted successfully.')
        return redirect('my_videos')
    return redirect('my_videos')


def review_video(request, video_id):
    if not request.user.is_staff:
        return redirect('dashboard')
    if request.method == "POST":
        status = request.POST['status']
        if status == "approve":
            review_video = VideoRecord.objects.get(pk=video_id)
            if review_video is not None:
                review_video.status = True
                user = int(request.user.id)
                review_video.admin_id = User(pk=user)
                review_video.save()
                messages.success(request, 'Video has been approved')
                return redirect('view_all_video')
            messages.error(request, 'Video do not exist in our record')
            return redirect('view_all_video')
        else:
            decline_video = VideoRecord.objects.get(pk=video_id)
            if decline_video is not None:
                user = int(request.user.id)
                decline_video.admin_id = User(pk=user)
                decline_video.save()
                messages.error(request, 'Video has been declined')
                return redirect('view_all_video')
            messages.error(request, 'Video do not exist in our record')
            return redirect('view_all_video')

    review_video = VideoRecord.objects.get(pk=video_id)
    context = {'review_video':review_video}
    return render(request, 'dashboard/review_video.html', context)




# Process and redirect login form data
@login_required(login_url="/accounts/login")
def record(request):
    return render(request, 'dashboard/video_recording.html')

# Process and redirect login form data
@login_required(login_url="/accounts/login")
def record_two(request):
    return render(request, 'dashboard/video_recording_two.html')






@login_required(login_url="/accounts/login")
def change_image(request):
    data = {'message': 'Something went wrong with your form data',
            'status': 'failed'}
    if request.method == "POST":
        user = request.user.id
        change_image = User.objects.get(pk=user)
        change_image.avatar = request.FILES['avatar']
        change_image.save()
        status = User.objects.get(pk=user)
        data = {
            'message':'Profile image has been updated',
            'status':'success',
            'avatar': str(status.avatar),
        }
    return JsonResponse(data)
        


