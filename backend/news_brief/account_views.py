from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings as django_settings


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

from .models import UserPreference, ReadingHistory, Notification, SupportTicket, Article

class UserSettingsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        pref, _ = UserPreference.objects.get_or_create(user=request.user)
        return Response({'theme': pref.theme, 'text_size': pref.text_size})
        
    def put(self, request):
        pref, _ = UserPreference.objects.get_or_create(user=request.user)
        pref.theme = request.data.get('theme', pref.theme)
        pref.text_size = request.data.get('text_size', pref.text_size)
        pref.save()
        return Response({'theme': pref.theme, 'text_size': pref.text_size})

class ReadingHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        history = ReadingHistory.objects.filter(user=request.user)[:50]
        data = [{
            'id': h.article.id,
            'title': h.article.title,
            'source': h.article.publisher.name if getattr(h.article, 'publisher', None) else 'ByteBrief',
            'viewed_at': h.viewed_at.isoformat()
        } for h in history]
        return Response(data)
        
    def post(self, request):
        article_id = request.data.get('article_id')
        if not article_id:
            return Response({'error': 'no article_id'}, status=400)
        try:
            article = Article.objects.get(id=article_id)
            ReadingHistory.objects.update_or_create(user=request.user, article=article)
            return Response({'status': 'ok'})
        except Article.DoesNotExist:
            return Response({'error': 'Article not found'}, status=404)

class NotificationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        notifs = Notification.objects.filter(user=request.user).order_by('-created_at')[:20]
        data = [{
            'id': n.id, 'title': n.title, 'message': n.message,
            'is_read': n.is_read, 'created_at': n.created_at.isoformat()
        } for n in notifs]
        return Response(data)
        
    def post(self, request):
        notif_id = request.data.get('notification_id')
        try:
            n = Notification.objects.get(id=notif_id, user=request.user)
            n.is_read = True
            n.save()
            return Response({'status': 'ok'})
        except Notification.DoesNotExist:
            return Response({'error': 'not found'}, status=404)

class SupportTicketView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        subject = request.data.get('subject')
        message = request.data.get('message')
        ticket_type = request.data.get('type', 'General')  # 'Problem' or 'Contact'
        if not subject or not message:
            return Response({'error': 'subject and message required'}, status=400)
        
        ticket = SupportTicket.objects.create(user=request.user, subject=subject, message=message)
        
        # Send email notification to ByteBrief support
        SUPPORT_EMAIL = 'bytebrief2026@gmail.com'
        email_subject = f'[ByteBrief {ticket_type}] {subject}'
        email_body = (
            f"New {ticket_type} ticket from {request.user.email} ({request.user.get_full_name() or request.user.username})\n"
            f"{'='*50}\n\n"
            f"Subject: {subject}\n"
            f"Type: {ticket_type}\n\n"
            f"Message:\n{message}\n\n"
            f"{'='*50}\n"
            f"Ticket ID: {ticket.id}\n"
            f"User: {request.user.email}\n"
        )
        try:
            send_mail(
                email_subject,
                email_body,
                django_settings.DEFAULT_FROM_EMAIL,
                [SUPPORT_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass  # Don't fail the ticket creation if email fails
        
        return Response({'status': 'Ticket submitted. Our team will get back to you soon!'})
