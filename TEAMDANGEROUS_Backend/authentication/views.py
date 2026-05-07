from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

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
            if not user.is_active:
                return Response({"error": "ACCESS BLOCKED // ACCOUNT SUSPENDED"}, status=status.HTTP_403_FORBIDDEN)
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'status': 'ACCESS GRANTED'
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "ACCESS DENIED: INVALID SIGNATURE"}, status=status.HTTP_401_UNAUTHORIZED)

class VerifyView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_active:
            return Response({"error": "BLOCKED"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"status": "ACTIVE", "username": request.user.username})
