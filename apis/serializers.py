import uuid

from rest_framework import serializers
from .models import ParadoxUser, Referral, Questions, Hints, Profile
from django.contrib.auth.hashers import mask_hash


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Paradox User Model
    """
    ref_code = serializers.CharField(read_only=True)

    class Meta:
        model = ParadoxUser
        fields = "__all__"

    def create(self, validated_data):
        name = validated_data['name']
        email = validated_data['email']
        validated_data['ref_code'] = name[0:3] + str(uuid.uuid1()).split('-')[0][:6]
        return super().create(validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for Question Model
    """

    class Meta:
        model = Questions
        fields = "__all__"


class HintSerializer(serializers.ModelSerializer):
    """
    Serializer for Hint Model
    """

    class Meta:
        model = Hints
        fields = "__all__"


class ReferralSerializer(serializers.ModelSerializer):
    """
    Serializer for Referral Model
    """

    class Meta:
        model = Referral
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile Model
    """

    class Meta:
        model = Profile
        fields = "__all__"


class LeaderBoardSerializer(serializers.ModelSerializer):
    """
    Serializer for LeaderBoard
    """

    class Meta:
        model = Profile
        exclude = ['reg_time', 'attempts', 'coins', 'super_coins']
