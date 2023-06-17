from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# from polls.views import PollListView, PollDetailView, PollResultsView
from .views import CreatePollView, PollDetailView

app_name = 'polls'
urlpatterns = [
    path('', views.PollListView.as_view(), name='list'),
    path('<int:poll_id>/', PollDetailView.as_view(), name='detail'),
    path('<int:poll_id>/results/', views.PollResultsView.as_view(), name='results'),
    path('create/', CreatePollView.as_view(), name='create'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='polls:list'), name='logout'),
    path('register/', views.register, name='register'),
    
]
