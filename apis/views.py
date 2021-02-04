from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from .serializers import UserSerializer, LeaderBoardSerializer, ProfileSerializer, QuestionSerializer, HintSerializer, \
    RefferalSerializer, ExeMembersSerializer, UserHintLevelSerializer, AnswerSerializer, UpdateCoinSerializer, \
    MessageSerializer, UserDetailsSerializer, ExeMembersPositionListSerializer, IsUserPresentSerializer
from .models import Profile, Referral, ParadoxUser, Questions, Hints, ExeMembers, UserHintLevel


class UserView(GenericAPIView):
    """
    User ViewSet
    """
    serializer_class = UserSerializer

    response_schema_dict = {
        "200": openapi.Response(
            description="User is Created.",
            schema=UserSerializer,
            examples={
                "application/json": {
                    "google_id": "rwkjgerwrgertglbget",
                    "ref_code": "Done18440",
                    "name": "Donald Trump",
                    "email": "abcd@gmail.com"
                }
            }
        ),
        "400": openapi.Response(
            description="When Error Occurs",
            schema=UserSerializer,
            examples={
                "application/json": {
                    "google_id": [
                        "This field may not be blank."
                    ],
                    "name": [
                        "This field may not be blank."
                    ],
                    "email": [
                        "This field may not be blank."
                    ]
                }
            }
        ),
        "500": openapi.Response(
            description="Internal Server Error",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "Internal Server Error"
                }
            }
        )
    }

    @swagger_auto_schema(responses=response_schema_dict)
    def post(self, request):
        """
        ## POST Method To Create User in Database.
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
            user_hint_level = UserHintLevel.objects.create(
                user=user,
                level=1,
                hintNumber=0
            )
            user_hint_level.save()
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
    response_schema_dict = {
        "200": openapi.Response(
            description="Users List In Sorted Order Based on Score For LeaderBoard.",
            schema=LeaderBoardSerializer,
            examples={
                "application/json": [
                    {
                        "user": "1223123434343",
                        "name": "195516@nith.ac.in",
                        "image": "https://storage.googleapis.com/sport_application/running%205.jpg",
                        "level": 1,
                        "score": 0,
                        "coins": 550,
                        "refferral_availed": False
                    },
                    {
                        "user": "12231234343mj43",
                        "name": "1955168@nith.ac.in",
                        "image": "https://storage.googleapis.com/sport_application/running%205.jpg",
                        "level": 1,
                        "score": 0,
                        "coins": 100,
                        "refferral_availed": True
                    }]
            }
        ),
        "500": openapi.Response(
            description="Internal Server Error",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "Internal Server Error"
                }
            }
        )
    }

    @swagger_auto_schema(responses=response_schema_dict)
    def get(self, request):
        """
        ## Retrieve LeaderBoard
        """
        try:
            return Response(LeaderBoardSerializer(self.get_queryset(), many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileDetailsView(GenericAPIView):
    """
    Profile Detail View
    """
    serializer_class = ProfileSerializer

    response_schema_dict = {
        "200": openapi.Response(
            description="Users Detail",
            schema=UserDetailsSerializer,
            examples={
                "application/json": {
                    "google_id": "1223123434343",
                    "ref_code": "Mri525092",
                    "name": "Mrigank Anand",
                    "email": "195516@nith.ac.in",
                    "profile": {
                        "user": "1223123434343",
                        "name": "195516@nith.ac.in",
                        "image": "https://storage.googleapis.com/sport_application/running%205.jpg",
                        "reg_time": "2021-02-04T04:07:08.283313+05:30",
                        "level": 1,
                        "attempts": 0,
                        "score": 0,
                        "coins": 100,
                        "super_coins": 100,
                        "refferral_availed": False
                    }
                }
            }
        ),
        "404": openapi.Response(
            description="User not found.",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "User Not Found. Invalid google_id Provided"
                }
            }
        ),
        "500": openapi.Response(
            description="Internal Server Error",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "Internal Server Error"
                }
            }
        )
    }

    @swagger_auto_schema(responses=response_schema_dict)
    def get(self, request, google_id):
        """

        - ## Retrieve User Profile
        - ## Full Profile Using GoogleId provided by Google at the time of Sign-In Using Google.
        """
        try:
            if len(ParadoxUser.objects.filter(google_id=google_id)) == 0:
                return Response({"message": "User Not Found. Invalid google_id Provided"},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                response = UserSerializer(ParadoxUser.objects.get(google_id=google_id), many=False).data
                response['profile'] = ProfileSerializer(Profile.objects.get(user__google_id__exact=google_id),
                                                        many=False).data
                return Response(response, status.HTTP_200_OK)
        except:
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuestionView(GenericAPIView):
    """
    ## Question View
    """
    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()

    response_schema_dict = {
        "200": openapi.Response(
            description="Question List",
            schema=QuestionSerializer,
            examples={
                "application/json": [
                    {
                        "level": 1,
                        "location": "/img1.jpeg",
                        "answer": "apple"
                    },
                    {
                        "level": 2,
                        "location": "/img2.jpeg",
                        "answer": "Chess"
                    }
                ]
            }
        ),
        "500": openapi.Response(
            description="Internal Server Error",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "Internal Server Error"
                }
            }
        )
    }

    @swagger_auto_schema(responses=response_schema_dict)
    def get(self, request):
        """
        ## Retrieve all questions present in Paradox Game.
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

    response_schema_dict = {
        "200": openapi.Response(
            description="Hints List",
            schema=HintSerializer,
            examples={
                "application/json": [
                    {
                        "level": 1,
                        "hint1": "It's a fruit.",
                        "hint2": "It's of red color.",
                        "hint3": "It's found in hilly area."
                    },
                    {
                        "level": 2,
                        "hint1": "It is a Sport.",
                        "hint2": "Indoor Sport.",
                        "hint3": "Game was from india."
                    }
                ]
            }
        ),
        "500": openapi.Response(
            description="Internal Server Error",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "Internal Server Error"
                }
            }
        )
    }

    @swagger_auto_schema(responses=response_schema_dict)
    def get(self, request):
        """
        ## Retrieve List Of Hints Present in Paradox Game.
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

    response_schema_dict = {
        "200": openapi.Response(
            description="Hints List",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "Referral Successfully Availed"
                }
            }
        ),
        "400": openapi.Response(
            description="User Not Found, Invalid Referral Code, Trying to redeem referral for self.",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    'message': 'user has already availed referral points.'
                },
            }
        ),
        "500": openapi.Response(
            description="Internal Server Error",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "Internal Server Error"
                }
            }
        )
    }

    @swagger_auto_schema(responses=response_schema_dict)
    def post(self, request):
        """
        ## Post Method For Redeeming referral Points.
        """
        try:
            data = request.data
            serializer = RefferalSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user_profile = Profile.objects.get(user__google_id=serializer.validated_data['user'])
            referral = Referral.objects.get(ref_code=serializer.validated_data['ref_code'])
            if user_profile.refferral_availed:
                return Response({'message': 'user has already availed referral points.'},
                                status=status.HTTP_400_BAD_REQUEST)
            if referral.user.google_id == user_profile.user.google_id:
                return Response({'message': 'Cannot Avail Referral of yourself.'}, status=status.HTTP_400_BAD_REQUEST)
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


class ExeMemberView(ListAPIView, CreateAPIView):
    """
    Exe Member View
    """
    queryset = ExeMembers.objects.all()
    serializer_class = ExeMembersSerializer

    response_schema_dict1 = {
        "200": openapi.Response(
            description="Exe Member List",
            schema=ExeMembersSerializer,
            examples={
                "application/json":
                    [
                        {
                            "id": 1,
                            "name": "mrigank anand",
                            "position": "Developer",
                            "category": "Full Stack",
                            "image": "https://drive.google.com/file/d/1DlZ_NsfTCGZKDjsXeehOS55OsQ_oSWFz/view?usp=drivesdk",
                            "githubUrl": "https://github.com/spiderxm",
                            "linkedInUrl": "https://www.linkedin.com/in/mrigankanand/"
                        }
                    ]
            }
        ),
        "500": openapi.Response(
            description="Internal Server Error",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "Internal Server Error"
                }
            }
        )
    }

    response_schema_dict = {
        "200": openapi.Response(
            description="Exe Member Created Successfullt",
            schema=ExeMembersSerializer,
            examples={
                "application/json": {
                    "id": 1,
                    "name": "mrigank anand",
                    "position": "Developer",
                    "category": "Full Stack",
                    "image": "https://drive.google.com/file/d/1DlZ_NsfTCGZKDjsXeehOS55OsQ_oSWFz/view?usp=drivesdk",
                    "githubUrl": "https://github.com/spiderxm",
                    "linkedInUrl": "https://www.linkedin.com/in/mrigankanand/"
                }
            }
        ),
        "400": openapi.Response(
            description="Errors",
            schema=ExeMembersSerializer,
            examples={
                "application/json": {
                    "image": [
                        "Enter a valid URL."
                    ],
                    "githubUrl": [
                        "Enter a valid URL."
                    ],
                    "linkedInUrl": [
                        "Enter a valid URL."
                    ]
                }
            }
        ),
        "500": openapi.Response(
            description="Internal Server Error",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "Internal Server Error"
                }
            }
        )
    }

    @swagger_auto_schema(responses=response_schema_dict1)
    def get(self, request, *args, **kwargs):
        """
        ## List Exe Members
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(responses=response_schema_dict)
    def post(self, request, *args, **kwargs):
        """
        ## Create Exe Members
        """
        return super().post(request, *args, **kwargs)


class ExeMemberPositionsView(GenericAPIView):
    """
    ## Exe Member Position View
    """
    serializer_class = ExeMembersPositionListSerializer

    response_schema_dict = {
        "200": openapi.Response(
            description="Exe Member Positions List",
            schema=ExeMembersPositionListSerializer,
            examples={
                "application/json": ['Developer', 'Mentor', 'Final year', 'Coordinator', 'Executive', 'Volunteer']
            }
        ),
        "500": openapi.Response(
            description="Internal Server Error",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "Internal Server Error"
                }
            }
        )
    }

    @swagger_auto_schema(responses=response_schema_dict)
    def get(self, request):
        """
        ## Retrieve All Positions For Exe Members
        """
        return Response(['Developer', 'Mentor', 'Final year', 'Coordinator', 'Executive', 'Volunteer'],
                        status=status.HTTP_200_OK)


class DecreaseCoins(GenericAPIView):
    """
    Decrease coins of user when they avail Hints
    """
    serializer_class = UserHintLevelSerializer

    def post(self, request):
        """
        Decrease coins of user when they avail Hints
        """
        coins = {
            "1": 20,
            "2": 30,
            "3": 40
        }
        data = request.data
        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        hintDetails = UserHintLevel.objects.get(user__google_id=validated_data['google_id'])
        userProfile = Profile.objects.get(user__google_id=validated_data['google_id'])
        hintDetails.hintNumber += 1
        if userProfile.coins >= coins[str(hintDetails.level)]:
            userProfile.coins = userProfile.coins - coins[str(hintDetails.level)]
        else:
            return Response({"message": "Not sufficient coins."}, status=status.HTTP_400_BAD_REQUEST)
        hintDetails.save()
        userProfile.save()
        return Response({"message": "Updated User Coins."}, status=status.HTTP_200_OK)


class CheckAnswerView(GenericAPIView):
    """
    Check Answer View
    """
    serializer_class = AnswerSerializer

    response_schema_dict = {
        "200": openapi.Response(
            description="Correct Answer Response",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "Correct answer"
                }
            }
        ),
        "400": openapi.Response(
            description="Incorrect Answer Response",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "Incorrect answer"
                }
            }
        ),
        "500": openapi.Response(
            description="Internal Server Error",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "Internal Server Error"
                }
            }
        )
    }

    @swagger_auto_schema(responses=response_schema_dict)
    def post(self, request):
        """
        - ## Validate User Answer
        - ## Reward Points
        """
        try:
            data = request.data
            serializer = AnswerSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            question = Questions.objects.get(level=validated_data)
            if question.answer == validated_data.answer.strip():
                profile = Profile.objects.get(user__google_id=validated_data['google_id'])
                userHint = UserHintLevel.objects.get(user__google_id=validated_data['google_id'])
                profile.coins += 100
                profile.level += 1
                userHint.level = profile.level
                userHint.hintNumber = 0
                userHint.save()
                profile.save()
                return Response({"message": "Correct answer"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Incorrect answer"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserPresentView(GenericAPIView):
    """
    View to check user present or not
    """
    response_schema_dict = {
        "200": openapi.Response(
            description="User Found",
            schema=IsUserPresentSerializer,
            examples={
                "application/json": {
                    'userPresent': True
                }
            }
        ),
        "404": openapi.Response(
            description="User Not Found",
            schema=IsUserPresentSerializer,
            examples={
                "application/json": {
                    'userPresent': True
                }
            }
        ),
        "500": openapi.Response(
            description="Internal Server Error",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "Internal Server Error"
                }
            }
        )
    }
    serializer_class = IsUserPresentSerializer

    @swagger_auto_schema(responses=response_schema_dict)
    def get(self, request, google_id):
        """
        ## Get Method to check whether a User with a google Id is present in database or not.
        """
        try:
            if len(ParadoxUser.objects.filter(google_id=google_id)) > 0:
                return Response({'userPresent': True}, status=status.HTTP_200_OK)
            else:
                return Response({'userPresent': False}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateUserCoinsView(GenericAPIView):
    """
    Update User Coins
    """

    serializer_class = UpdateCoinSerializer
    response_schema_dict = {
        "200": openapi.Response(
            description="Successfully Updated Coins",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "Coins Updated"
                }
            }
        ),
        "400": openapi.Response(
            description="Errors",
            schema=UpdateCoinSerializer,
            examples={
                "application/json": {
                    "user": [
                        "User Not found. Invalid Google Id."
                    ]
                }
            }
        ),
        "500": openapi.Response(
            description="Internal Server Error",
            schema=MessageSerializer,
            examples={
                "application/json": {
                    "message": "Internal Server Error"
                }
            }
        )
    }

    @swagger_auto_schema(responses=response_schema_dict)
    def put(self, request):
        """
        - ## Put Request To Update User Coins
        - ## Can be Used by Frontend To reward users for watching rewarded advertisement.
        """
        try:
            data = request.data
            serializer = UpdateCoinSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            profile = Profile.objects.get(user__google_id=validated_data['google_id'])
            profile.coins += int(validated_data['coins'])
            profile.save()
            return Response({"message": "Coins Updated"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
