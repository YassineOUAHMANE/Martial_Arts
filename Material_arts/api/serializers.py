from rest_framework import serializers
from .models import User, MartialArt, Movement, PracticeSession, ProgressHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class MartialArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = MartialArt
        fields = "__all__"


class MovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movement
        fields = "__all__"


class PracticeSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeSession
        fields = "__all__"


class ProgressHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressHistory
        fields = "__all__"
