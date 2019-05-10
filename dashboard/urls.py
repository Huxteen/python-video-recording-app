from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import (
    dashboard,
    change_image,
    record_two,
    record,
    my_videos,
    delete_video,
    review_video,
    view_all_video,

    )

# URL for the dashboard app
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('record', record, name='record'),
    path('record_two', record_two, name='record_two'),
    path('change-image', change_image, name='change_image'),
    path('my-videos', my_videos, name='my_videos'),
    path('delete-video/<int:video_id>/', delete_video, name='delete_video'),
    path('review-video/<int:video_id>/', review_video, name='review_video'),
    path('view-all-video', view_all_video, name='view_all_video'),
]
   
