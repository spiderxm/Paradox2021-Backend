import uuid
from rest_framework import serializers
from .models import ParadoxUser, Referral, Questions, Hints, Profile, Rules, ExeMembers, UserHintLevel


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


class RuleSerializer(serializers.ModelSerializer):
    """
    Serializer for Rules Model
    """

    class Meta:
        model = Rules
        fields = "__all__"


class ExeMembersSerializer(serializers.ModelSerializer):
    """
    Serializer for Developer Model
    """

    class Meta:
        model = ExeMembers
        fields = "__all__"


class UserHintLevelSerializer(serializers.Serializer):
    """
    Serializer for Updating Hint Info
    """
    google_id = serializers.CharField()
    level = serializers.IntegerField()
    hintNumber = serializers.IntegerField(min_value=1, max_value=3)

    def validate(self, attrs):
        google_id = attrs.get('google_id')
        level = attrs.get('level')
        hintNumber = attrs.get('hintNumber')
        if not ParadoxUser.objects.filter(google_id=google_id).exists():
            raise serializers.ValidationError({'user': 'User Not found. Invalid Google Id.'})
        hintDetails = UserHintLevel.objects.get(user__google_id=google_id)
        if hintDetails.level == level:
            if hintDetails.hintNumber >= hintNumber:
                raise serializers.ValidationError({'user': ('User Has Already Redeemed the Hint.',)})
        else:
            raise serializers.ValidationError({'level': ('Invalid Level Number',)})
        return super().validate(attrs)


class AnswerSerializer(serializers.Serializer):
    """
    Serializer for checking answer
    """
    answer = serializers.CharField(max_length=255)
    google_id = serializers.CharField()
    level = serializers.IntegerField()

    def validate(self, attrs):
        google_id = attrs.get('google_id')
        if not ParadoxUser.objects.filter(google_id=google_id).exists():
            raise serializers.ValidationError({'user': 'User Not found. Invalid Google Id.'})

        return super().validate(attrs)


class UpdateCoinSerializer(serializers.Serializer):
    """
    Update Coin For User Serializer
    """
    google_id = serializers.CharField()
    coins = serializers.IntegerField(min_value=0, max_value=100)

    def validate(self, attrs):
        google_id = attrs.get('google_id')
        if not ParadoxUser.objects.filter(google_id=google_id).exists():
            raise serializers.ValidationError({'user': 'User Not found. Invalid Google Id.'})
        return super().validate(attrs)


class MessageSerializer(serializers.Serializer):
    """
    Message Serializer
    """
    message = serializers.CharField(max_length=255)


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for User Details (ParadoxUser model + Profile model) serializer
    """
    profile = ProfileSerializer()

    class Meta:
        model = ParadoxUser
        fields = "__all__"


class ExeMembersPositionListSerializer(serializers.Serializer):
    """
    Serializer for Exe Members Positions List
    """
    list = serializers.ListField()


class IsUserPresentSerializer(serializers.Serializer):
    """
    Serializer to check user present or not
    """
    userPresent = serializers.BooleanField()