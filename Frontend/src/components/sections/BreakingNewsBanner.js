import React, { useState } from 'react';
import { Zap } from 'lucide-react';
import { Link } from 'react-router-dom';

const BreakingNewsBanner = ({ breakingNews }) => {
  const [localIndex, setLocalIndex] = useState(0);

  if (!breakingNews || breakingNews.length === 0) return null;
  const newsItem = breakingNews[localIndex];

  return (
    <div className="bg-gradient-to-r from-red-600 via-purple-600 to-blue-600 p-3 overflow-hidden">
      <style>{`
        @keyframes marquee {
          0% { transform: translateX(100vw); }
          100% { transform: translateX(-100%); }
        }
        .animate-marquee {
          display: inline-flex;
          white-space: nowrap;
          animation: marquee 25s linear infinite;
        }
        .marquee-wrapper:hover .animate-marquee {
          animation-play-state: paused;
        }
      `}</style>
      <div className="flex items-center w-full px-4">
        <div className="flex flex-shrink-0 items-center space-x-2 mr-4 relative z-10 bg-gradient-to-r from-red-600 to-red-600/90 pr-2 pb-1 pt-1">
          <Zap className="h-4 w-4 text-white animate-pulse" />
          <span className="text-white font-semibold text-sm">BREAKING NEWS </span>
        </div>
        <div className="flex-1 overflow-hidden flex items-center h-6">
          <div 
            className="animate-marquee pl-4"
            onAnimationIteration={() => setLocalIndex((prev) => (prev + 1) % breakingNews.length)}
          >
            <Link
              to={`/article/${newsItem.id || localIndex}`}
              state={{ article: newsItem }}
              className="text-white text-sm hover:text-cyan-200 transition-colors"
            >
              <span className="font-bold mr-2 text-cyan-400">•</span>
              {newsItem.title}
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BreakingNewsBanner;