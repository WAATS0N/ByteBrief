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

import os
import logging
from django.conf import settings
from django.http import HttpResponse, FileResponse

logger = logging.getLogger(__name__)

def ping(request):
    """Health check endpoint"""
    return JsonResponse({"status": "alive", "message": "ByteBrief Backend is operational"})

def serve_react(request, path=''):
    """
    Custom catch-all view to serve React's index.html from any of the configured 
    Frontend build directories. This is more robust than TemplateView for 
    high-traffic production apps.
    """
    # Prefer relative to BASE_DIR if settings.TEMPLATES is configured correctly
    for template_dir in settings.TEMPLATES[0]['DIRS']:
        index_path = Path(template_dir) / 'index.html'
        if index_path.exists():
            return FileResponse(open(index_path, 'rb'))
    
    # Fallback to direct path checks if TEMPLATES is empty or failing
    paths_to_check = [
        settings.BASE_DIR.parent / 'Frontend' / 'build' / 'index.html',
        settings.BASE_DIR.parent / 'frontend' / 'build' / 'index.html',
    ]
    
    for p in paths_to_check:
        if p.exists():
            return FileResponse(open(p, 'rb'))
            
    logger.error(f"FAIL: React index.html not found! Checked: {[str(p) for p in paths_to_check]}")
    return HttpResponse(
        "<h1>ByteBrief: Frontend Build Missing</h1><p>The application is running but the React build artifacts were not found. Check deployment logs.</p>", 
        status=404
    )

    adapter_class = GoogleOAuth2Adapter
    callback_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
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
                { "name": 'Startups & Innovation', "icon": "Rocket", "color": 'from-red-500 to-orange-500', "count": 14 },
                { "name": 'AI & Future Tech', "icon": "Cpu", "color": 'from-cyan-500 to-blue-500', "count": 42 },
                { "name": 'Climate & Environment', "icon": "Leaf", "color": 'from-emerald-500 to-green-500', "count": 16 },
                { "name": 'Cybersecurity', "icon": "Shield", "color": 'from-slate-600 to-slate-400', "count": 12 },
                { "name": 'Digital Life', "icon": "Smartphone", "color": 'from-pink-500 to-rose-400', "count": 10 },
                { "name": 'Space & Research', "icon": "Satellite", "color": 'from-violet-500 to-fuchsia-500', "count": 9 },
                { "name": 'Psychology & Mind', "icon": "Brain", "color": 'from-indigo-400 to-blue-600', "count": 11 },
                { "name": 'Global Affairs', "icon": "Globe", "color": 'from-blue-600 to-indigo-800', "count": 21 },
                { "name": 'Entertainment', "icon": "Music", "color": 'from-fuchsia-500 to-purple-500', "count": 19 },
                { "name": 'Science', "icon": "Sparkles", "color": 'from-teal-500 to-cyan-500', "count": 15 },
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

from django.db.models import Q

@csrf_exempt
def generate_digest_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.body else {}
            keywords = data.get('keywords', [])
            categories = data.get('categories', [])
            sources = data.get('sources', [])

            # Fetch recent articles from DB (last 48 hours to keep it fresh)
            time_threshold = timezone.now() - timedelta(days=90)  # Extended to 90 days so existing articles are always included
            qs = DBArticle.objects.select_related('publisher').filter(published_at__gte=time_threshold)
            
            if keywords:
                # Combine keywords with OR logic for title and summary
                q_objects = Q()
                for keyword in keywords:
                    q_objects |= Q(title__icontains=keyword) | Q(summary__icontains=keyword) | Q(content__icontains=keyword)
                qs = qs.filter(q_objects)
            
            qs = qs.order_by('-published_at')
            
            # For simplicity matching the old keyword/category filter format
            articles = []
            if categories:
                # Case-insensitive match: URL params arrive as 'tech', DB stores 'Tech'
                cat_lower = [c.lower() for c in categories]
                filtered_qs = [a for a in qs if (a.category or '').lower() in cat_lower]
            else:
                filtered_qs = list(qs)[:100]  # Return top 100 if no category selected
                
            for a in filtered_qs:
                articles.append({
                    'id': a.id,
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

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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
            data = request.data
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

from .models import Bookmark

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_bookmarks_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)

    if request.method == 'GET':
        bookmarks = Bookmark.objects.filter(user=request.user).select_related('article')
        data = []
        for b in bookmarks:
            a = b.article
            data.append({
                'id': a.id,
                'title': a.title,
                'content': a.summary or a.content,
                'source': a.publisher.name if a.publisher else 'Unknown',
                'url': a.url,
                'image_url': a.image_url,
                'published_date': a.published_at.strftime("%Y-%m-%d %H:%M:%S") if a.published_at else None,
                'category': a.category or 'Global',
                'bookmarked_at': b.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        return JsonResponse({
            'status': 'success',
            'bookmarks': data
        })

    elif request.method == 'POST':
        try:
            data = request.data
            # We assume frontend passes an article_id to bookmark
            article_id = data.get('article_id')
            # It could also pass a URL if the article isn't guaranteed to be the DB ID...
            article_url = data.get('article_url')

            article = None
            if article_id:
                article = DBArticle.objects.get(id=article_id)
            elif article_url:
                article = DBArticle.objects.get(url=article_url)
                
            if not article:
                return JsonResponse({'status': 'error', 'message': 'Article not found'}, status=404)

            # Create the bookmark
            Bookmark.objects.get_or_create(user=request.user, article=article)
            return JsonResponse({'status': 'success', 'message': 'Article bookmarked'})
        except DBArticle.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Article not found in database'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    elif request.method == 'DELETE':
        try:
            data = request.data
            article_id = data.get('article_id')
            article_url = data.get('article_url')
            
            if article_id:
                Bookmark.objects.filter(user=request.user, article_id=article_id).delete()
            elif article_url:
                Bookmark.objects.filter(user=request.user, article__url=article_url).delete()
                
            return JsonResponse({'status': 'success', 'message': 'Bookmark removed'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

import threading
from django.core.management import call_command

@csrf_exempt
def force_scrape_api(request):
    """
    Hidden webhook to manually trigger database import/scrape without needing Render Shell.
    Just visit: /api/admin/force-scrape/
    """
    if request.method == 'GET':
        def run_scrape():
            try:
                print("Starting regional sources import...")
                call_command('import_regional_sources')
                print("Starting manual scrape...")
                call_command('scrape_news')
                print("Scrape finished successfully!")
            except Exception as e:
                print(f"Scrape webhook failed: {str(e)}")
                
        # Run in background thread so the HTTP request doesn't timeout
        thread = threading.Thread(target=run_scrape)
        thread.start()
        
        return JsonResponse({
            'status': 'success', 
            'message': 'Scraper has been triggered in the background! Please wait 2-3 minutes, then refresh your site.'
        })
    return JsonResponse({'status': 'error', 'message': 'Only GET is supported'}, status=405)

from django.contrib.auth import get_user_model

@csrf_exempt
def clear_users_api(request):
    """
    Hidden webhook to manually remove all non-superuser accounts from the database.
    Just visit: /api/admin/clear-users/
    """
    if request.method == 'GET':
        try:
            User = get_user_model()
            # Delete everyone except superusers
            count, _ = User.objects.filter(is_superuser=False).delete()
            return JsonResponse({
                'status': 'success',
                'message': f'Successfully wiped {count} user accounts from the database.'
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Only GET is supported'}, status=405)
