from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import UserSerializer, LeaderBoardSerializer, ProfileSerializer
from .models import Profile, Referral, ParadoxUser


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
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LeaderBoardView(GenericAPIView):
    serializer_class = LeaderBoardSerializer
    queryset = Profile.objects.all().order_by('-score')

    def get(self, request):
        try:
            return Response(LeaderBoardSerializer(self.get_queryset(), many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileDetailsView(GenericAPIView):

    def get(self, request, google_id):
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
