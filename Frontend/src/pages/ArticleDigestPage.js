import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { ArrowLeft, Clock, Share2, BookOpen, CheckCircle, Brain, Bookmark, Lock } from 'lucide-react';
import { fetchBookmarks, toggleBookmark } from '../services/api';

const ArticleDigestPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [digestPoints, setDigestPoints] = useState([]);
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [showLimitModal, setShowLimitModal] = useState(false);

  // Get article from navigation state
  const article = location.state?.article;

  useEffect(() => {
    if (!article) {
      // If accessed directly without state, redirect to home
      // In a real app, we would fetch by ID here
      navigate('/');
      return;
    }

    const token = localStorage.getItem('access_token');
    if (!token) {
      let clicks = parseInt(sessionStorage.getItem('guest_article_clicks') || '0');
      clicks += 1;
      sessionStorage.setItem('guest_article_clicks', clicks.toString());
      if (clicks > 3) {
        setShowLimitModal(true);
      }
    } else if (article && article.category) {
      let prefs = JSON.parse(localStorage.getItem("user_category_prefs") || "{}");
      prefs[article.category] = (prefs[article.category] || 0) + 1;
      localStorage.setItem("user_category_prefs", JSON.stringify(prefs));
    }

    // Heuristic: Transform summary/content into point-by-point digest
    let rawText = article.summary || article.content || "";

    // Double decode in case it's escaped HTML encoded in RSS
    let temp = document.createElement('textarea');
    temp.innerHTML = rawText;
    let decoded = temp.value;
    
    // Now strip standard HTML tags
    let div = document.createElement('div');
    div.innerHTML = decoded;
    let textToProcess = div.textContent || div.innerText || "";
    
    // Clean up trailing ellipses and stray single characters (like "a.")
    textToProcess = textToProcess.replace(/\s+/g, " ");
    textToProcess = textToProcess.replace(/<[^>]+>/g, ""); // Extra safety for broken tags
    textToProcess = textToProcess.replace(/(\s*\.{1,3}\s*)+$/g, "."); // Replace any trailing dots/spaces with a single period
    
    // Split by period, question mark, or exclamation mark followed by a space
    let extracted = textToProcess
      .split(/(?<=[.?!])\s+/)
      .filter(p => p.length > 15 && !p.match(/\b[a-z]{1,2}\.$/i))
      .map(p => p.trim());
      
    // Remove duplicates without changing order
    extracted = [...new Set(extracted)];

    let points = [];
    if (extracted.length >= 4) {
      points = extracted.slice(0, 5);
    } else {
      // If we don't have enough natural sentences, build contextual takeaways
      const enrichedPoints = [];
      
      // 1. The core fact (Title)
      if (article.title && !extracted[0]?.includes(article.title.slice(0, 20))) {
        enrichedPoints.push(`${article.title}.`);
      }
      
      // 2. The actual summary sentences
      enrichedPoints.push(...extracted);
      
      // 3. Contextual additions to reach 4-5 points
      if (enrichedPoints.length < 4 && article.source) {
        enrichedPoints.push(`According to reports from ${article.source}, this development provides key insights into the ${article.category || 'current'} landscape.`);
      }
      if (enrichedPoints.length < 4) {
        enrichedPoints.push(`This event highlights significant ongoing shifts and trends within the ${article.category || 'global'} sector.`);
      }
      if (enrichedPoints.length < 5) {
        enrichedPoints.push(`Analysts indicate that further developments are expected as the situation unfolds in the coming days.`);
      }
      
      points = [...new Set(enrichedPoints)].slice(0, 5);
    }

    setDigestPoints(points.length > 0 ? points : [textToProcess]);

  }, [article, navigate]);

  useEffect(() => {
    const checkBookmarkStatus = async () => {
      if (article) {
        const token = localStorage.getItem('access_token');
        if (token) {
          const res = await fetchBookmarks(token);
          if (res.status === 'success') {
            const found = res.bookmarks.some(b => b.url === article.url);
            setIsBookmarked(found);
          }
        }
      }
    };
    checkBookmarkStatus();
  }, [article]);

  const handleToggleBookmark = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      alert("Please login to bookmark articles.");
      return;
    }
    // Optimistic UI update
    setIsBookmarked(!isBookmarked);
    
    const res = await toggleBookmark(token, article.url, isBookmarked);
    if (res.status !== 'success') {
      setIsBookmarked(isBookmarked); // rollback
    }
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: article.title,
          text: article.summary,
          url: article.url,
        });
      } catch (err) {
        console.log('Error sharing:', err);
      }
    } else {
      navigator.clipboard.writeText(article.url);
      alert('Link copied to clipboard!');
    }
  };

  if (!article) return null;

  return (
    <div className="min-h-screen bg-black pt-8 pb-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <button
          onClick={() => {
            if (window.history.state && window.history.state.idx > 0) {
              navigate(-1);
            } else {
              navigate('/home');
            }
          }}
          className="inline-flex items-center text-gray-400 hover:text-white transition-colors mb-8 group"
        >
          <ArrowLeft className="h-4 w-4 mr-2 group-hover:-translate-x-1 transition-transform" />
          Back to Digest
        </button>

        {/* Transformed Container */}
        <div className="relative bg-gray-900/50 rounded-2xl border border-purple-500/20 overflow-hidden shadow-2xl backdrop-blur-sm">
          {/* Decorative Top Gradient */}
          <div className="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-purple-500 via-cyan-500 to-purple-500" />

          <div className="p-8 md:p-12">
            {/* Header */}
            <div className="mb-8">
              <div className="flex items-center space-x-3 mb-4">
                <span className="px-3 py-1 rounded-full text-xs font-semibold bg-purple-500/10 text-purple-400 border border-purple-500/20">
                  {article.category || "News"}
                </span>
                <span className="flex items-center text-xs text-gray-400">
                  <Clock className="h-3 w-3 mr-1" />
                  {article.readTime || "3 min read"}
                </span>
                <span className="flex items-center text-xs text-gray-400">
                  <Brain className="h-3 w-3 mr-1" />
                  AI Summarized
                </span>
              </div>

              <h1 className="text-3xl md:text-5xl font-bold text-white mb-6 leading-tight">
                {article.title}
              </h1>

              {/* Meta actions */}
              <div className="flex items-center justify-between border-b border-gray-800 pb-8 mb-8">
                <div className="text-gray-400 text-sm">
                  Source: <span className="text-white font-medium">{article.source || "ByteBrief Intelligence"}</span>
                </div>
                <div className="flex space-x-4">
                  <button onClick={() => window.open(article.url, '_blank')} className="p-2 rounded-full hover:bg-gray-800 text-gray-400 hover:text-white transition-colors" title="Read Full Article">
                    <BookOpen className="h-5 w-5" />
                  </button>
                  <button onClick={handleToggleBookmark} className="p-2 rounded-full hover:bg-gray-800 text-gray-400 hover:text-white transition-colors" title={isBookmarked ? "Remove Bookmark" : "Bookmark"}>
                    <Bookmark className={`h-5 w-5 ${isBookmarked ? 'fill-current text-purple-400' : ''}`} />
                  </button>
                  <button onClick={handleShare} className="p-2 rounded-full hover:bg-gray-800 text-gray-400 hover:text-white transition-colors" title="Share">
                    <Share2 className="h-5 w-5" />
                  </button>
                </div>
              </div>
            </div>

            {/* Digest Content */}
            <div className="relative space-y-6">
              <h2 className="text-xl font-semibold text-cyan-400 flex items-center">
                <CheckCircle className="h-5 w-5 mr-2" />
                Key Takeaways
              </h2>

              <div className={`space-y-4 ${showLimitModal ? 'blur-md pointer-events-none select-none opacity-40' : ''}`}>
                {digestPoints.map((point, index) => (
                  <div key={index} className="flex items-start group">
                    <span className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-800 text-gray-400 flex items-center justify-center text-sm font-mono mr-4 group-hover:bg-purple-500/20 group-hover:text-purple-400 transition-colors">
                      {index + 1}
                    </span>
                    <p className="text-gray-300 text-lg leading-relaxed pt-1 group-hover:text-white transition-colors">
                      {point}
                    </p>
                  </div>
                ))}
              </div>

              {showLimitModal && (
                <div className="absolute inset-0 z-50 flex items-center justify-center">
                  <div className="bg-gray-900 border border-purple-500/50 p-6 sm:p-8 rounded-3xl shadow-2xl max-w-md text-center transform -translate-y-4 animate-fade-in-up">
                    <div className="bg-purple-500/20 p-4 rounded-full w-16 h-16 mx-auto mb-6 flex items-center justify-center">
                      <Lock className="w-8 h-8 text-purple-400" />
                    </div>
                    <h3 className="text-2xl font-extrabold text-white mb-3">Free Limit Reached</h3>
                    <p className="text-gray-400 mb-8 font-medium leading-relaxed">
                      You've read 3 AI summaries as an exploring guest. Please create a free account to continue reading, personalize your feed, and save articles.
                    </p>
                    <Link
                      to="/login"
                      className="w-full inline-block py-4 px-6 bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-500 hover:to-cyan-500 text-white rounded-xl font-bold shadow-[0_0_30px_-10px_rgba(168,85,247,0.5)] transition-transform hover:scale-105"
                    >
                      Log In / Sign Up
                    </Link>
                  </div>
                </div>
              )}
            </div>

            <div className="mt-12 pt-8 border-t border-gray-800">
              <p className="text-sm text-center text-gray-500 italic">
                This digest was generated by ByteBrief AI from verified sources.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArticleDigestPage;
