import uuid

from rest_framework import serializers
from .models import ParadoxUser, Referral, Questions, Hints, Profile


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
        exclude = ['reg_time', 'attempts', 'super_coins']


class RefferalSerializer(serializers.Serializer):
    """
    Serializer For Referral
    """
    ref_code = serializers.CharField(required=True)
    user = serializers.CharField(required=True)

    def validate(self, attrs):
        ref_code = attrs.get('ref_code')
        user = attrs.get('user')
        if not Referral.objects.filter(ref_code=ref_code).exists():
            raise serializers.ValidationError({'ref_code': ('Invalid Referral Code')})
        if not ParadoxUser.objects.filter(google_id=user).exists():
            raise serializers.ValidationError({'user': ('Invalid Google Id')})
        return super().validate(attrs)
