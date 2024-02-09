from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer, OtpVerificationSerializer
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.generics import GenericAPIView
from .models import User
from .email import *
from .serializers import ResetPasswordEmailSerializer, UserResetPasswordSerializer


class UserRegisterView(
    GenericAPIView,
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "id"

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        send_otp_via_email(serializer.data['email'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EmailVerificationview(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = OtpVerificationSerializer(data=data)
            if serializer.is_valid():
                otp = serializer.validated_data['otp']
                user = User.objects.filter(otp=otp).first() 

                if user:
                    user.is_verified = True
                    user.save()

                    return Response({
                        'status': 200,
                        'msg': "Successfully Verified",
                        'data': serializer.data
                    })
                else:
                    return Response({
                        'status': 400,
                        'msg': "Not Verified",
                        'data': {'otp': ['Invalid OTP']}
                    })
            else:
                return Response({
                    'status': 400,
                    'msg': "Invalid data",
                    'data': serializer.errors
                })
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'msg': "Internal Server Error"
            })

class UserResetPasswordEmailView(APIView):
    serializer_class = ResetPasswordEmailSerializer

    def post(self, request, format=None):
        serializer = ResetPasswordEmailSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Reset link send. Please check your Email"},
            status=status.HTTP_200_OK,
        )

class ResetPasswordView(APIView):
    serializer_class = UserResetPasswordSerializer

    def post(self, request, uid, token, format=None):
        serializer = UserResetPasswordSerializer(
            data=request.data, context={'uid': uid, "token": token}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Reset Successfully"}, status=status.HTTP_200_OK
        )
