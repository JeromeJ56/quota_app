from django.urls import path

from . import views

urlpatterns = [
    
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('questions/', views.question_list, name='question_list'),
    path('questions/ask/', views.ask_question, name='ask_question'),
    path('questions/<int:pk>/', views.question_detail, name='question_detail'),
    path('answers/<int:answer_id>/like/', views.like_answer, name='like_answer'),
]