"""
URL configuration for realtimefaceatten project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('student_register',views.student_details,name='student_register'),
    path('views_student',views.view_student,name='views_student'),
    path('attendance',views.attendance,name='attendance'),
    path('take_attendance',views.take_attendance,name='take_attendance'),
    # path('video_feed/', views.videoFeed, name='video_feed'),
    # path('face_attendance/', views.faceAttendance, name='face_attendance'),
    # path('get_video/', views.getVideo, name='get_video'),
    path('search_attendance',views.search_attendance,name='search_attendance'),
    path('searchtable',views.searchtable,name='searchtable'),
    path('myprofile',views.myprofile,name='myprofile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)