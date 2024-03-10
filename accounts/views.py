from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


@method_decorator(csrf_exempt, name='dispatch')
class SignupView(views.APIView):
    """
    API endpoint for user registration.

    Allows any user (including unauthenticated users) to sign up.

    URL: /signup/
    """
    def post(self, request):
        """
        Handle POST request for user registration.

        Parameters:
        - username (str): User's username.
        - password (str): User's password.
        - email (str): User's email address.

        Returns:
        - JSON Response: Success message or error message.
        """
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')
            if not username or not password:
                raise ValueError('Username and password are required.')
            User.objects.create_user(username=username, password=password, email=email)
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': f'An unexpected error occurred.{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SigninView(views.APIView):
    """
    API endpoint for user authentication and token generation.

    Allows any user (including unauthenticated users) to sign in.

    URL: /signin/
    """
    def post(self, request):
        """
        Handle POST request for user authentication.

        Parameters:
        - email (str): User's email address.
        - password (str): User's password.

        Returns:
        - JSON Response: Access and refresh tokens or error message.
        """
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            if not email or not password:
                raise ValueError('Both username and password are required.')
            user = User.objects.filter(email=email).first()
            if user is None or not user.check_password(password):
                raise ValueError('Invalid credentials.')
            refresh = RefreshToken.for_user(user)
            user = authenticate(email=email, password=password)
            if user is not None:
                # login(request, user)
                print(request.user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_401_UNAUTHORIZED)
