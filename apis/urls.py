from rest_framework.urls import path
from .views import UserView, LeaderBoardView, ProfileDetailsView, QuestionView, \
    HintsView, ReferralView

urlpatterns = [
    path('user/', UserView.as_view()),
    path('leaderboard/', LeaderBoardView.as_view()),
    path('userProfile/<str:google_id>/', ProfileDetailsView.as_view()),
    path('questions/', QuestionView.as_view()),
    path('hints/', HintsView.as_view()),
    path('refferral/', ReferralView.as_view())
]
