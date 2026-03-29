import React, { useState, useEffect } from 'react';
import { Clock, ArrowRight, Share2, Bookmark } from 'lucide-react';
import { Link } from 'react-router-dom';
import { fetchBookmarks, toggleBookmark } from '../../services/api';

// Define a bulletproof, instantly-loading SVG data URI fallback for broken images
const FALLBACK_IMAGE = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='600' viewBox='0 0 800 600'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' stop-color='%231e1b4b' /%3E%3Cstop offset='100%25' stop-color='%233b0764' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='100%25' height='100%25' fill='url(%23g)' /%3E%3Ctext x='50%25' y='50%25' font-family='sans-serif' font-size='48' font-weight='bold' fill='%23a78bfa' text-anchor='middle' dominant-baseline='middle'%3EByteBrief%3C/text%3E%3C/svg%3E";

const FeaturedNews = ({ featuredArticles }) => {
  const [bookmarks, setBookmarks] = useState({});

  useEffect(() => {
    const loadBookmarks = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        const res = await fetchBookmarks(token);
        if (res.status === 'success') {
          const bMap = {};
          res.bookmarks.forEach(b => {
            bMap[b.url] = true;
          });
          setBookmarks(bMap);
        }
      }
    };
    loadBookmarks();
  }, []);

  const handleToggleBookmark = async (article) => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      alert("Please login to bookmark articles.");
      return;
    }
    const isBookmarked = bookmarks[article.url];
    setBookmarks(prev => ({ ...prev, [article.url]: !isBookmarked }));
    
    const res = await toggleBookmark(token, article.url, isBookmarked);
    if (res.status !== 'success') {
      setBookmarks(prev => ({ ...prev, [article.url]: isBookmarked }));
    }
  };

  const handleShare = async (article) => {
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

  return (
    <div className="py-20 bg-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-white mb-12 flex items-center">
          <span className="bg-purple-500 w-2 h-8 mr-4 rounded-full"></span>
          Featured Digest
        </h2>

        <div className="grid grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-8">
          {featuredArticles.map((article) => {
            return (
              <div key={article.id} className="group relative bg-gray-900/50 rounded-2xl border border-gray-800 overflow-hidden hover:border-purple-500/50 transition-all duration-300">
                <div className="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-purple-500 to-cyan-500 opacity-0 group-hover:opacity-100 transition-opacity z-10"></div>

                <div className="w-full aspect-video overflow-hidden bg-gray-800">
                  <img
                    src={article.image_url || FALLBACK_IMAGE}
                    alt=""
                    loading="lazy"
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    onError={(e) => { 
                      e.target.onerror = null; 
                      e.target.src = FALLBACK_IMAGE; 
                    }}
                  />
                </div>

                <div className="p-4 sm:p-6 md:p-8">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-4 sm:mb-6 gap-2">
                    <span className="self-start px-2 py-1 md:px-3 md:py-1 rounded-full text-[10px] md:text-xs font-semibold bg-gray-800 text-gray-300 border border-gray-700">
                      {article.category}
                    </span>
                    <div className="flex items-center space-x-2 md:space-x-3 self-end sm:self-auto">
                      <span className={`text-[10px] md:text-xs font-bold ${article.importance > 8 ? 'text-red-400' : 'text-purple-400'}`}>
                        {article.sentiment === 'positive' ? 'High Impact' : 'Trending'}
                      </span>
                      <button onClick={() => handleToggleBookmark(article)} className="focus:outline-none">
                        <Bookmark
                          className={`h-3 w-3 md:h-4 md:w-4 cursor-pointer transition-colors ${bookmarks[article.url] ? 'fill-current text-purple-400' : 'text-gray-500 hover:text-white'}`}
                        />
                      </button>
                    </div>
                  </div>

                  <h3 className="text-base sm:text-lg md:text-2xl font-bold text-white mb-2 md:mb-4 leading-tight group-hover:text-purple-400 transition-colors line-clamp-3">
                    <Link to={`/article/${article.id}`} state={{ article }}>
                      {article.title}
                    </Link>
                  </h3>

                  <p className="text-xs sm:text-sm text-gray-400 mb-4 md:mb-6 line-clamp-2 md:line-clamp-3">
                    {(() => {
                      const text = article.summary || article.content || "No summary available.";
                      // Double decode in case it's escaped HTML encoded in RSS
                      let temp = document.createElement('textarea');
                      temp.innerHTML = text;
                      let decoded = temp.value;
                      let div = document.createElement('div');
                      div.innerHTML = decoded;
                      return (div.textContent || div.innerText || "").replace(/<[^>]+>/g, "").trim() || "No summary available.";
                    })()}
                  </p>

                  <div className="flex flex-col sm:flex-row sm:items-center justify-between pt-4 md:pt-6 border-t border-gray-800 gap-3">
                    <div className="flex items-center text-[10px] md:text-sm text-gray-500">
                      <Clock className="h-3 w-3 md:h-4 w-4 mr-1 md:mr-2" />
                      {article.readTime}
                    </div>

                    <div className="flex items-center space-x-3 md:space-x-4">
                      <button onClick={() => handleShare(article)} className="text-gray-500 hover:text-white transition-colors">
                        <Share2 className="h-3 w-3 md:h-4 w-4" />
                      </button>
                      <Link
                        to={`/article/${article.id}`}
                        state={{ article }}
                        className="flex items-center text-[10px] sm:text-xs md:text-base text-purple-400 font-semibold group-hover:translate-x-1 transition-transform whitespace-nowrap"
                      >
                        Read Digest <ArrowRight className="h-3 w-3 md:h-4 w-4 ml-1 md:ml-2" />
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default FeaturedNews;