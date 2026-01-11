import React from 'react';
import { Clock } from 'lucide-react';

const FeaturedNews = ({ featuredArticles }) => (
  <div className="py-20 bg-black">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h2 className="text-3xl font-bold text-white text-center mb-12">
        Today's Top Stories
      </h2>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {featuredArticles.map((article, index) => (
          <div
            key={article.id}
            className={`bg-gradient-to-br ${
              index === 0 
                ? 'from-purple-900/50 to-cyan-900/50 lg:col-span-2 lg:row-span-2' 
                : 'from-gray-800/50 to-gray-900/50'
            } backdrop-blur-xl rounded-xl p-6 border border-purple-500/20 hover:border-purple-400/40 transition-all duration-300 cursor-pointer group`}
          >
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs bg-purple-500/20 text-purple-300 px-3 py-1 rounded-full">
                {article.category}
              </span>
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${
                  article.sentiment === 'positive' ? 'bg-green-400' : 
                  article.sentiment === 'negative' ? 'bg-red-400' : 'bg-yellow-400'
                }`}></div>
                <span className="text-xs text-gray-400">Score: {article.importance}</span>
              </div>
            </div>
            <h3 className={`${index === 0 ? 'text-2xl' : 'text-lg'} font-bold text-white mb-3 group-hover:text-purple-300 transition-colors`}>
              {article.title}
            </h3>
            <p className="text-gray-300 mb-4 line-clamp-3">
              {article.summary}
            </p>
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-400">{article.readTime}</span>
              <Clock className="h-4 w-4 text-gray-500" />
            </div>
          </div>
        ))}
      </div>
    </div>
  </div>
);

export default FeaturedNews;