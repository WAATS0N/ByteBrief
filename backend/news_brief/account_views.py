from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate


class UserProfileView(APIView):
    """GET user profile, PATCH to update name fields."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'pk': user.pk,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'date_joined': user.date_joined.isoformat(),
        })

    def patch(self, request):
        user = request.user
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.save()
        return Response({
            'pk': user.pk,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'date_joined': user.date_joined.isoformat(),
        })


class DeleteAccountView(APIView):
    """Permanently delete a user account after password confirmation."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        password = request.data.get('password', '')
        user = request.user

        if not user.check_password(password):
            return Response(
                {'error': 'Incorrect password. Account not deleted.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.delete()
        return Response({'message': 'Account deleted successfully.'})
