from rest_framework import serializers
from .models import Question, User, Card, Update


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "current_round", "password",)

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "current_round")

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = "__all__"
