from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        try:
            if User.objects.filter(username=data['username']).exists():
                return Response({"error": "USERNAME ALREADY EXISTS"}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(
                username=data['username'],
                email=data.get('email', ''),
                password=data['password'],
                first_name=data.get('full_name', ''),
                phone=data.get('phone', '')
            )
            return Response({"msg": "PROTOCOL INITIATED: USER REGISTERED"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'status': 'ACCESS GRANTED'
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "ACCESS DENIED: INVALID SIGNATURE"}, status=status.HTTP_401_UNAUTHORIZED)
