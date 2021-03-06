from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt

from .serializers.common import NestedUserSerializer, UserSerializer
from .serializers.populated import PopulatedUserSerializer

User = get_user_model()


class RegisterView(APIView):
    """ Controller for post request to /auth/register """

    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        if user_to_create.is_valid():
            user_to_create.save()
            return Response(
                {"message": "Registration Successful"}, status=status.HTTP_201_CREATED
            )
        return Response(
            user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class LoginView(APIView):

    """ Controller for post request to /auth/login """

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user_to_login = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied(detail="Invalid Credentials")
        if not user_to_login.check_password(password):
            raise PermissionDenied(detail="Invalid Credentials")
        expiry_time = datetime.now() + timedelta(days=7)
        token = jwt.encode(
            {"sub": user_to_login.id, "exp": int(expiry_time.strftime("%s"))},
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        return Response(
            {"token": token, "message": f"Welcome Back {user_to_login.username}"}
        )


class ProfileView(APIView):
    def get_user(self, pk):
        """ returns user from db by its pk(id) or responds 404 not found """
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound()

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        serialized_user = PopulatedUserSerializer(user)
        return Response(serialized_user.data, status=status.HTTP_200_OK)

    def put(self, request):
        user_to_update = self.get_user(pk=request.user.id)
        if user_to_update.id != request.user.id:
            raise PermissionDenied()
        updated_user = UserSerializer(user_to_update, data=request.data)
        if updated_user.is_valid():
            updated_user.save()
            return Response(updated_user.data, status=status.HTTP_202_ACCEPTED)
        return Response(
            updated_user.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class ProfileListView(APIView):
    def get(self, _request):
        users = User.objects.all()
        serialized_user = UserSerializer(users, many=True)
        return Response(serialized_user.data, status=status.HTTP_200_OK)


class ProfileDetailView(APIView):
    def get_user(self, pk):
        """ returns user from db by its pk(id) or responds 404 not found """
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound()

    def get(self, _request, pk):
        user = self.get_user(pk=pk)
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data, status=status.HTTP_200_OK)
