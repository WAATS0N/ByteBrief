from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import NewsBriefForm
import sys
from pathlib import Path
import json
from collections import defaultdict
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000"
    client_class = OAuth2Client

# Add src to path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from bytebrief.core.models import ClientConfig
from bytebrief.agent.orchestrator import AgentOrchestrator

@csrf_exempt
def get_metadata(request):
    if request.method == 'GET':
        data = {
            "categories": [
                { "name": 'Breaking', "icon": "Zap", "color": 'from-red-500 to-orange-500', "count": 12 },
                { "name": 'Tech', "icon": "Bot", "color": 'from-blue-500 to-purple-500', "count": 24 },
                { "name": 'Business', "icon": "TrendingUp", "color": 'from-green-500 to-teal-500', "count": 18 },
                { "name": 'Global', "icon": "Globe", "color": 'from-purple-500 to-pink-500', "count": 15 },
                { "name": 'Health', "icon": "Heart", "color": 'from-pink-500 to-rose-500', "count": 21 },
                { "name": 'Sports', "icon": "Trophy", "color": 'from-orange-500 to-yellow-500', "count": 19 },
                { "name": 'Politics', "icon": "Users", "color": 'from-indigo-500 to-blue-500', "count": 16 },
                { "name": 'Finance', "icon": "DollarSign", "color": 'from-emerald-500 to-green-500', "count": 14 },
                { "name": 'Travel', "icon": "Plane", "color": 'from-sky-500 to-cyan-500', "count": 8 },
                { "name": 'Gaming', "icon": "Gamepad2", "color": 'from-violet-500 to-purple-500', "count": 11 },
            ],
            "stats": [
                { "label": 'News Sources', "value": '10+', "icon": "Globe" },
                { "label": 'Articles Daily', "value": '100+', "icon": "TrendingUp" },
                { "label": 'AI Accuracy', "value": '97%', "icon": "Bot" },
                { "label": 'Read Time Saved', "value": '85%', "icon": "Clock" }
            ],
            "hero": {
                "title": "ByteBrief",
                "subtitle": "Smart News Digest Generator",
                "animatedText": "Smart News Digest Generator",
                "features": [
                    { "icon": "Bot", "title": "AI-Powered", "description": "Advanced algorithms analyze and summarize news from hundreds of sources" },
                    { "icon": "Zap", "title": "Real-Time", "description": "Get breaking news and updates as they happen, 24/7 monitoring" },
                    { "icon": "Sparkles", "title": "Personalized", "description": "Customized digests based on your interests and reading preferences" }
                ]
            }
        }
        return JsonResponse(data)
    return JsonResponse({'status': 'error', 'message': 'Only GET method allowed'}, status=405)

from .models import Article as DBArticle, UserPreference
from django.utils import timezone
from datetime import timedelta

@csrf_exempt
def generate_digest_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.body else {}
            keywords = data.get('keywords', [])
            categories = data.get('categories', [])
            sources = data.get('sources', [])

            # Fetch recent articles from DB (last 48 hours to keep it fresh)
            time_threshold = timezone.now() - timedelta(days=2)
            qs = DBArticle.objects.select_related('publisher').filter(published_at__gte=time_threshold).order_by('-published_at')
            
            # For simplicity matching the old keyword/category filter format
            articles = []
            if categories:
                cat_lower = [c.lower() for c in categories]
                filtered_qs = [a for a in qs if (a.category or '').lower() in cat_lower]
            else:
                filtered_qs = list(qs)[:100]  # Return top 100 if no category selected
                
            for a in filtered_qs:
                articles.append({
                    'title': a.title,
                    'content': a.summary or a.content,
                    'source': a.publisher.name if a.publisher else 'Unknown',
                    'url': a.url,
                    'image_url': a.image_url,
                    'published_date': a.published_at.strftime("%Y-%m-%d %H:%M:%S") if a.published_at else None,
                    'category': a.category or 'Global',
                })

            # Group articles by category for the frontend
            by_category = {}
            for article in articles:
                cat = str(article.get('category') or 'Global')
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(article)

            return JsonResponse({
                'status': 'success',
                'articles': articles,
                'by_category': by_category,
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)

@csrf_exempt
def user_preferences_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)
        
    if request.method == 'GET':
        pref, created = UserPreference.objects.get_or_create(user=request.user)
        return JsonResponse({
            'status': 'success',
            'categories': pref.categories
        })
        
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            categories = data.get('categories', [])
            pref, created = UserPreference.objects.get_or_create(user=request.user)
            pref.categories = categories
            pref.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Preferences updated',
                'categories': pref.categories
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
