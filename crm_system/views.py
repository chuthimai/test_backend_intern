from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from drf_spectacular.utils import extend_schema, OpenApiResponse
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

@extend_schema(
    summary="Trang chủ API",
    description="API này có thể được truy cập mà không cần đăng nhập.",
    responses={200: OpenApiResponse(description="Welcome to API demo.")}
)
@api_view(["GET"])
@permission_classes([AllowAny])
def home(request):
    return HttpResponse("Welcome to API demo.")


@extend_schema(
    summary="Đăng ký tài khoản",
    description="API này cho phép tạo tài khoản mới mà không cần đăng nhập.",
    responses={
        200: OpenApiResponse(description="Registration successful!"),
        400: OpenApiResponse(description="Email already exists!")
    }
)
@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def register_view(request):
    if request.method == "GET":
        return render(request, "register.html")

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if User.objects.filter(email=email).exists():
        messages.error(request, "Email already exists!")
        return render(request, "register.html")

    user = User.objects.create_user(username=username, email=email, password=password)

    if user:
        messages.success(request, "Registration successful!")
        return redirect("login")

    messages.error(request, "Registration failed!")
    return render(request, "register.html")


@extend_schema(
    summary="Đăng nhập (Không cần xác thực)",
    description="POST: API này xác thực người dùng và trả về JWT token."
                "\n GET: Trả về trang login",
    responses={
        200: OpenApiResponse(description="Trả về access_token và refresh_token"),
        401: OpenApiResponse(description="Invalid email or password"),
    }
)
@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")

    email = request.data.get("email")
    password = request.data.get("password")

    user = User.objects.filter(email=email).first()

    if user and check_password(password, user.password):
        tokens = get_tokens_for_user(user)
        return Response({
            "access_token": str(tokens["access"]),
            "refresh_token": str(tokens["refresh"])
        })

    messages.error(request, "Invalid email or password")
    return render(request, "login.html")


@extend_schema(
    summary="Đăng xuất",
    description="API này đăng xuất người dùng bằng cách blacklist refresh token.",
    responses={
        200: OpenApiResponse(description="Đã đăng xuất thành công."),
        400: OpenApiResponse(description="Invalid token")
    }
)
@api_view(["POST"])
@permission_classes([AllowAny])
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
