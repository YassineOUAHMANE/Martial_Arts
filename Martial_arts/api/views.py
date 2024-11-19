from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User, MartialArt, Movement, PracticeSession, ProgressHistory
from .serializers import (
    UserSerializer,
    MartialArtSerializer,
    MovementSerializer,
    PracticeSessionSerializer,
    ProgressHistorySerializer,
)
from .movement_correction import load_reference_sequence, provide_real_time_feedback




class MartialArtView(APIView):
    def get(self, request):
        martial_arts = MartialArt.objects.all()
        serializer = MartialArtSerializer(martial_arts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MartialArtSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovementView(APIView):
    def get(self, request, martial_art_id):
        movements = Movement.objects.filter(martial_art_id=martial_art_id)
        serializer = MovementSerializer(movements, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PracticeSessionView(APIView):
    def post(self, request):
        serializer = PracticeSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProgressHistoryView(APIView):
    def get(self, request, user_id):
        progress_history = ProgressHistory.objects.filter(user_id=user_id)
        serializer = ProgressHistorySerializer(progress_history, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProgressHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AnalyzeMovementView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        movement_id = request.data.get("movement_id")
        live_video = request.data.get("live_video", False)
        alert_sound_path = "beep.mp3"  # Path to your alert sound file

        # Get user and movement objects
        user = get_object_or_404(User, user_id=user_id)
        movement = get_object_or_404(Movement, movement_id=movement_id)
        reference_file_path = movement.reference_file.path

        try:
            # Load reference sequence and analyze movement
            reference_sequence = load_reference_sequence(reference_file_path)
            result = provide_real_time_feedback(
                movement.name,
                video_path=None if live_video else request.data.get("video_path"),
                reference_sequences_file=reference_file_path,
                deviation_threshold=0.1,
                alert_sound_path=alert_sound_path,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save practice session and progress history
        practice_session = PracticeSession.objects.create(
            movement=movement,
            user=user,
            score=result["score"],
            user_feedback=result["feedback"],
        )
        progress_history = ProgressHistory.objects.create(
            user=user,
            movement=movement,
            session=practice_session,
            progress_score=result["score"],
        )

        return Response(
            {
                "session_id": practice_session.session_id,
                "score": result["score"],
                "feedback": result["feedback"],
                "progress_id": progress_history.history_id,
            },
            status=status.HTTP_201_CREATED,
        )
