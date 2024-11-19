from django.urls import path
from .views import (
    MartialArtView,
    MovementView,
    PracticeSessionView,
    UserView,
    ProgressHistoryView,
    AnalyzeMovementView,
)

urlpatterns = [
    path("martial-arts/", MartialArtView.as_view(), name="martial-arts"),
    path("martial-arts/<int:martial_art_id>/movements/", MovementView.as_view(), name="movements"),
    path("practice-sessions/", PracticeSessionView.as_view(), name="practice-sessions"),
    path("users/", UserView.as_view(), name="users"),
    path("progress-history/<int:user_id>/", ProgressHistoryView.as_view(), name="progress-history"),
    path("analyze-movement/", AnalyzeMovementView.as_view(), name="analyze-movement"),  # New endpoint
]