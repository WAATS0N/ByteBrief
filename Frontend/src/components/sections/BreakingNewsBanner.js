import React from 'react';
import { Zap } from 'lucide-react';
import { Link } from 'react-router-dom';

const BreakingNewsBanner = ({ breakingNews, newsIndex }) => {
  const newsItem = breakingNews[newsIndex];
  if (!newsItem) return null;

  return (
    <div className="bg-gradient-to-r from-red-600 via-purple-600 to-blue-600 p-3 mt-16">
      <div className="flex items-center space-x-4 max-w-7xl mx-auto px-4">
        <div className="flex items-center space-x-2">
          <Zap className="h-4 w-4 text-white animate-pulse" />
          <span className="text-white font-semibold text-sm">BREAKING NEWS </span>
        </div>
        <div className="flex-1 overflow-hidden">
          <Link
            to={`/article/${newsItem.id}`}
            state={{ article: newsItem }}
            className="text-white text-sm animate-pulse hover:text-gray-200 transition-colors block truncate"
          >
            {newsItem.title}
          </Link>
        </div>
      </div>
    </div>
  );
};

export default BreakingNewsBanner;