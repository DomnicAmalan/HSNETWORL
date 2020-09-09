from django.urls import path

from . import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path('phone-auth', views.phoneAuth, name='phoneAuth'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('submit', views.formSubmit, name='submit'),
    path('submit/edit/<str:job_id>', views.editSubmit, name='editsubmit'),
    path('admin', views.admin, name='admin'),
    path('deletejob/<str:job_id>', views.deleteJob, name='delete'),
    path('editjob/<str:job_id>', views.editjob, name='edit'),
    path('viewfile/<str:file_id>', views.ViewFile, name='viewfile'),
    path('deletefile/<str:file_id>/job/<str:job_id>', views.DeleteFile, name='deletefile')
]