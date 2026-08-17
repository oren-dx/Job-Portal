from django.urls import path
from.views import *

urlpatterns = [
    path('',register,name='register'),
    path('login/',login_page,name='login_page'),
    path('logout/',logout_page,name='logout_page'),

    path('dashboard/',dashboard,name='dashboard'),
    path('profile-view/',profile_view,name='profile_view'),
    path('update-profile/',update_profile,name='update_profile'),
    path('job-details/<int:id>/',job_details,name='job_details'),
    
    path('browse-job/',browse_job,name='browse_job'),
    path('post-job/',post_job,name='post_job'),
    path('update-job/<str:id>/',update_JobPost,name='update_JobPost'),
    path('delete-job/<str:id>/',delete_JobPost,name='delete_JobPost'),
    
    path('apply-job/<str:id>/',apply_job,name='apply_job'),
    path('my-application/',my_application,name='my_application'),
    path('candidate-list/<str:id>/',candidate_list,name='candidate_list'),
    
    path('application/<int:application_id>/accept/',accept_application,name='accept_application'),
    path('application/<int:application_id>/reject/',reject_application,name='reject_application'),
]