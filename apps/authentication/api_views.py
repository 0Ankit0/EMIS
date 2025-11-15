"""
Authentication API Views
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    """User registration"""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """Get/Update user profile"""
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user


class ChangePasswordAPIView(generics.UpdateAPIView):
    """Change user password"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get('old_password')):
                return Response(
                    {'old_password': ['Wrong password.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            user.set_password(serializer.data.get('new_password'))
            user.save()
            
            return Response({'message': 'Password updated successfully'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
