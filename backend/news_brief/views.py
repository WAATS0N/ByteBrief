from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import NewsBriefForm
import sys
from pathlib import Path
import json

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
                { "label": 'News Sources', "value": '500+', "icon": "Globe" },
                { "label": 'Articles Daily', "value": '10K+', "icon": "TrendingUp" },
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

@csrf_exempt
def generate_digest_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            keywords = data.get('keywords', [])
            categories = data.get('categories', [])
            sources = data.get('sources', [])
            
            # Combine categories into keywords for better search
            search_keywords = list(keywords)
            if categories:
                search_keywords.extend(categories)
            
            client_config = ClientConfig(
                name="Guest",
                keywords=search_keywords,
                preferred_sources=sources,
                output_format='json',
                categories=categories
            )
            
            orchestrator = AgentOrchestrator()
            results_json = orchestrator.run(client_config)
            
            try:
                articles = json.loads(results_json)
            except:
                articles = []
                
            return JsonResponse({'status': 'success', 'articles': articles})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)


