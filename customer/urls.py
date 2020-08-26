from django.urls import path

from . import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path('phone-auth', views.phoneAuth, name='phoneAuth'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('submit', views.formSubmit, name='submit'),
    path('admin', views.admin, name='admin')
]