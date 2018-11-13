import jwt, json

from rest_framework import status, generics
from rest_framework.generics import views
from rest_framework.response import Response

from users.models import User
from users.serializers import UserAuthSerializer, UserProfileSerializer
from users.authentication import JWTAuthentication


# Create your views here.

class RetrieveUserAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    authentication_classes = (JWTAuthentication,)
    lookup_field = 'pk'

    def get_queryset(self):
        return User.objects.get(pk=self.lookup_field)


class Register(views.APIView):

    def post(self, request, *args, **kwargs):
        serialized = UserAuthSerializer(data=request.data)
        if serialized.is_valid():
            try:
                User.objects.get(
                    username=serialized.initial_data['username'],
                    email=serialized.intiial_data['email'],
                    password=serialized.initial_data['password'],
                )
                return Response({
                    "Error": "This user already exists."
                })
            except User.DoesNotExist:
                User.objects.create_user(
                    username=serialized.initial_data['username'],
                    email=serialized.initial_data['email'],
                    password=serialized.initial_data['password']
                )
                return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class Login(views.APIView):

    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response({"Error": "Please provide username/password"}, status="400")

        username = request.data['username']
        password = request.data['password']
        try:
            user = User.objects.get(username, password)
        except User.DoesNotExist:
            return Response({"Error": "Invalid username or password"}, status="400")

        if user:
            payload = {
                'id': user.id,
                'email': user.email
            }
            jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}
            serialized_user = UserAuthSerializer(user)

            return Response({
                "user": serialized_user,
                "token": jwt_token
            },
                status=200,
                content_type='application/json'
            )
        else:
            return Response(json.dumps({'Error': 'Invalid credentials'}),
                            status=400,
                            content_type="application/json")


class Logout(views.APIView):
    authentication_classes = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        return Response({
            "Success": True,
            "Message": "You are now logged out!"
        })
