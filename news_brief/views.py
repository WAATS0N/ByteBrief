from django.shortcuts import render
from .forms import NewsBriefForm
import sys
from pathlib import Path
import json

# Add src to path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "src"))

from bytebrief.core.models import ClientConfig
from bytebrief.agent.orchestrator import AgentOrchestrator

def index(request):
    if request.method == 'POST':
        form = NewsBriefForm(request.POST)
        if form.is_valid():
            # Create client config from form data
            keywords = [k.strip() for k in form.cleaned_data['keywords'].split(',')] if form.cleaned_data['keywords'] else []
            
            # Add categories to keywords for search context
            categories = form.cleaned_data['categories']
            if categories:
                # If keywords exist, we might want to combine them or treat them separately
                # For now, let's append categories to keywords so the orchestrator searches for them too
                keywords.extend(categories)
            
            client_config = ClientConfig(
                name="Guest",
                keywords=keywords,
                preferred_sources=form.cleaned_data['sources'],
                output_format='json',
                categories=categories
            )
            
            # Run agent
            orchestrator = AgentOrchestrator()
            results_json = orchestrator.run(client_config)
            
            try:
                articles = json.loads(results_json)
            except:
                articles = []
                
            return render(request, 'news_brief/results.html', {'articles': articles, 'config': client_config})
    else:
        form = NewsBriefForm()
    
    return render(request, 'news_brief/index.html', {'form': form})
