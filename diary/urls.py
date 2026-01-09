from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'diary'

urlpatterns = [
    path('', views.home, name='home'),
    path('diary/create/', views.create, name='create'),
    path('diary/<int:diary_id>/', views.detail, name='detail'),
    path('diary/<int:diary_id>/question/<int:question_id>/save/', views.save_answer, name='save_answer'),
    path('logout/', LogoutView.as_view(), name='logout'),
]