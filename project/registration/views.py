from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSerializer


User = get_user_model()


@swagger_auto_schema(
    methods=['POST'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['email', 'username', 'password', 'phone_number'],
    ),
    responses={
        201: 'Created',
        400: 'Bad Request',
    },
)
@authentication_classes([SessionAuthentication, BasicAuthentication])
@api_view(['POST'])
@permission_classes([AllowAny])
def registration_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.create(request.data)

        # Установите пароль для пользователя
        user.set_password(request.data['password'])
        user.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'message': 'Registration successful'})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    methods=['POST'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['username', 'password'],
    ),
    responses={
        200: 'Ok',
        401: 'Unauthorized',
    },
)
@ensure_csrf_cookie
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({'message': 'Login successful'})
        response.set_cookie('access_token', access_token, httponly=True)
        response.set_cookie('refresh_token', str(refresh), httponly=True)

        return response
    else:
        return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(
    methods=['POST'],
    responses={
        200: 'OK',
    },
)
@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    # Вызываем logout для аутентификации
    logout(request)

    # Удаляем куки из ответа
    response = Response({'message': 'Logout successful'})
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    return response
