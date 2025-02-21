import hashlib
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@permission_classes([AllowAny])
def home(request):
    return HttpResponse("Welcome to API demo.")


@permission_classes([AllowAny])
@api_view(['POST', 'GET'])
def register_view(request):
    if request.method == "GET":
        return render(request, "register.html")

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if User.objects.filter(email=email).exists():
        messages.error(request, "Email already exists!")
        return render(request, "register.html")

    hashed_password = make_password(password)  # Mã hóa mật khẩu đúng cách

    user = User.objects.create_user(username=username, email=email, password=hashed_password)

    if user:
        messages.success(request, "Registration successful!")
        return redirect("login")

    return render(request, "register.html")


@permission_classes([AllowAny])
@api_view(['POST', 'GET'])
def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")

    email = request.data.get("email")
    password = request.data.get("password")

    user = User.objects.filter(email=email).first()

    if user and check_password(password, user.password):
        tokens = get_tokens_for_user(user)
        response = redirect("schema")
        response.set_cookie("access_token", tokens["access"])  # Lưu token vào cookie
        return response

    messages.error(request, "Invalid email or password")
    return render(request, "login.html")


@api_view(["POST"])
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Đưa token vào danh sách blacklist

        response = redirect("login")
        response.delete_cookie("access_token")  # Xóa token khỏi cookie
        response.delete_cookie("refresh_token")
        return response
    except Exception:
        return Response(
            {"error": "Invalid token"},
            status=status.HTTP_400_BAD_REQUEST
        )
