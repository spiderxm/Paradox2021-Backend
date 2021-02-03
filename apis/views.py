from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import UserSerializer, LeaderBoardSerializer, ProfileSerializer, QuestionSerializer, HintSerializer, \
    RefferalSerializer
from .models import Profile, Referral, ParadoxUser, Questions, Hints


class UserView(GenericAPIView):
    """
    User ViewSet
    """
    serializer_class = UserSerializer

    def post(self, request):
        """
        POST Method To Create User in Database.
        """
        try:
            serializer = UserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            user = ParadoxUser.objects.get(google_id=serializer.validated_data['google_id'])
            # Create User Profile Related To User
            profile = Profile.objects.create(
                user=user,
                name=user.name,
            )
            # Create Referral Related To User
            referral = Referral.objects.create(
                user=user,
                ref_code=user.ref_code
            )
            profile.save()
            referral.save()
            return Response(UserSerializer(user, many=False).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LeaderBoardView(GenericAPIView):
    """
    LeaderBoard View
    """
    serializer_class = LeaderBoardSerializer
    queryset = Profile.objects.all().order_by('-score')

    def get(self, request):
        """
        Retrieve LeaderBoard
        """
        try:
            return Response(LeaderBoardSerializer(self.get_queryset(), many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileDetailsView(GenericAPIView):
    """
    Profile Detail View
    """
    serializer_class = ProfileSerializer

    def get(self, request, google_id):
        """
        Retrieve User Profile
        """
        try:
            if len(ParadoxUser.objects.filter(google_id=google_id)) == 0:
                return Response({"message": "User Not Found. Invalid google_id Provided"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                response = UserSerializer(ParadoxUser.objects.get(google_id=google_id), many=False).data
                response['profile'] = ProfileSerializer(Profile.objects.get(user__google_id__exact=google_id),
                                                        many=False).data
                return Response(response, status.HTTP_200_OK)
        except:
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuestionView(GenericAPIView):
    """
    Question View
    """
    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()

    def get(self, request):
        """
        Retrieve Questions
        """
        try:
            return Response(QuestionSerializer(self.get_queryset(), many=True).data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HintsView(GenericAPIView):
    """
    Hints View
    """
    serializer_class = HintSerializer
    queryset = Hints.objects.all()

    def get(self, request):
        """
        Retrieve Hints
        """
        try:
            return Response(HintSerializer(self.get_queryset(), many=True).data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReferralView(GenericAPIView):
    """
    Referral View
    """
    serializer_class = RefferalSerializer

    def post(self, request):
        """
        Post Method For Redeeming referral Points.
        """
        try:
            data = request.data
            serializer = RefferalSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user_profile = Profile.objects.get(user__google_id=serializer.validated_data['user'])
            referral = Referral.objects.get(ref_code=serializer.validated_data['ref_code'])
            if user_profile.refferral_availed:
                return Response({'user': ['user has already availed referral points.']},
                                status=status.HTTP_400_BAD_REQUEST)
            if referral.user.google_id == user_profile.user.google_id:
                return Response({'reg_code': 'Cannot Avail Referral of yourself.'}, status=status.HTTP_400_BAD_REQUEST)
            user_profile.coins += 100
            user_profile.refferral_availed = True
            user_profile.save()
            referral = Referral.objects.get(ref_code=serializer.validated_data['ref_code'])
            referral.ref_success += 1
            referral.save()
            profile_of_refferer = Profile.objects.get(user__google_id=referral.user.google_id)
            profile_of_refferer.coins += 100
            profile_of_refferer.save()
            return Response({"message": "Referral Successfully Availed"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
