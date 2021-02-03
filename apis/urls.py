from rest_framework.urls import path
from .views import UserView, LeaderBoardView, ProfileDetailsView

urlpatterns = [
    path('user/', UserView.as_view()),
    path('leaderboard/', LeaderBoardView.as_view()),
    path('userProfile/<str:google_id>/', ProfileDetailsView.as_view())
]
